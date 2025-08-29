import json
from library.connector import SisterSession, BearerAuth
from library.io import SisterIO
from library.api_spec import SisterSpec
from library.cache import SisterCache
from settings import *



class WebService(SisterIO, SisterCache):

    def __init__(self):
        SisterCache.__init__(self)
        self.session = SisterSession()
        self.spec = SisterSpec()
        self.config  = self.read_config()
        self.token_expired_datetime = {"minutes": 60}
        
        # Use environment variables for cache configuration
        self.cache_expired_datetime = {"days": ENV_CONFIG['cache_expiration_days']}
        
        self.use_cache()
        self.read_and_validate_api()
        
        # Enable auto cleanup if configured
        if ENV_CONFIG['auto_cleanup_cache']:
            self.enable_auto_cleanup(True)


    def use_cache(self, status=True):
        self.caching_system = status


    def read_and_validate_api(self):
        try:
            self.api_key = self.read_api_key()
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            # Remove corrupted API key file and create new one
            if os.path.exists(API_KEY_FILE):
                try:
                    os.remove(API_KEY_FILE)
                except OSError as e:
                    print(f"Error removing corrupted API key file: {e}")
            self.api_key = {}
        except Exception as e:
            print(f"Unexpected error reading API key: {e}")
            self.api_key = {}


    def request_api_key(self):
        response = self.response_template()
        if not self.check_config():
            response['message'] = 'Config or API is not valid'
            return self.parse_response(response)
        auth_data   = self.get_auth_data()
        get_api_key = self.session.post(f"{self.get_ws_url()}/authorize", json=auth_data)
        if self.is_json(get_api_key.text):
            json_api_key = get_api_key.json()
            if get_api_key.status_code == STATUS_SUCCESS:
                self.update_api_key(
                    token = json_api_key['token'],
                    role  = json_api_key['role'],
                    accessed_at = self.get_now_datetime(isoformat=True),
                    expired_at  = self.get_expired_datetime(isoformat=True, **self.token_expired_datetime),
                )
                response['data'] = json_api_key
            else:
                response['message'] = json_api_key['message']
                response['detail'] = json_api_key['detail']
        else:
            response['message'] = "Response is not in JSON format, check your URL"
        return self.parse_response(response)
        

    def get_response(self, connector, path, attr, response, fresh_api_key, **kwargs):
        content_type = connector.headers.get('Content-Type')
        response['content-type'] = content_type
        if content_type == 'application/json':
            json_object = connector.json()
            if connector.status_code in [STATUS_SUCCESS, STATUS_SUCCESS_NO_REPLY]:
                response['data'] = json_object
            elif connector.status_code in [STATUS_TOKEN_INVALID]:
                if fresh_api_key:
                    response['message'] = "API key invalid, check your credential"
                    return self.parse_response(response)
                self.request_api_key()
                return self.get_data(path, True, **kwargs)
            else:
                response['message'] = json_object['message']
                response['detail']  = json_object['detail']
        else:
            response['message'] = "Response is not in JSON format"
            # if response is byte/binnary like image
            response['data'] = connector.content
        return self.parse_response(response)


    def connect(self, method, path_url):
        method    = method.lower()
        connector = self.session
        if method == HTTP_METHOD_GET:
            connector = connector.get
        elif method == HTTP_METHOD_POST:
            connector = connector.post
        elif method == HTTP_METHOD_PATCH:
            connector = connector.patch
        elif method == HTTP_METHOD_DELETE:
            connector = connector.delete
        api_token = self.api_key.get('token')
        if not api_token:
            # request again when unavailable
            self.request_api_key()
            api_token = self.api_key.get('token')
        response = connector(path_url, auth=BearerAuth(api_token))
        return response
            


    def get_data(self, path, fresh_api_key=False, **kwargs):
        # Input validation
        if not path or not isinstance(path, str):
            response = self.response_template()
            response['message'] = 'Invalid path parameter'
            return self.parse_response(response)
            
        response = self.response_template()
        path_url = self.parse_path_url(path, **kwargs)

        # set default response
        response['cache'] = False
        response['accessed_at'] = self.get_now_datetime()
        response['expired_at']  = self.get_expired_datetime(**self.cache_expired_datetime)
        response['accessed_at_iso'] = str(response['accessed_at'])
        response['expired_at_iso']  = str(response['expired_at'])

        # check whether authorization is success or not
        if not self.api_key:
            api_key = self.request_api_key()
            if not api_key['status'] == True:
                return api_key        
            self.read_and_validate_api()

        # Auto-cleanup expired cache (optional, can be disabled)
        if hasattr(self, 'auto_cleanup_cache') and self.auto_cleanup_cache:
            self.cleanup_expired_cache()

        # check from cache
        cache_available = self.get_cache(path_url.name())
        if cache_available.get('data'):
            response['data'] = cache_available.get('data')
            accessed_at = self.iso_to_datetime(cache_available.get('accessed_at'))
            expired_at  = self.iso_to_datetime(cache_available.get('expired_at'))
            if self.get_now_datetime() < expired_at:
                # update response when using cache
                response['cache'] = True
                response['accessed_at'] = accessed_at
                response['expired_at']  = expired_at
                response['accessed_at_iso'] = str(accessed_at)
                response['expired_at_iso']  = str(expired_at)
                return response

        # check api-key expiration
        token_expired_time = self.api_key.get('expired_at')
        if token_expired_time:
            token_expired_time = self.iso_to_datetime(token_expired_time)
            if self.get_now_datetime() > token_expired_time:
                self.request_api_key()

        # read and validate API Key again
        self.read_and_validate_api()
        method, attr = self.spec.get_path_method_and_attr(path)
        connector = self.connect(method, path_url)
        response  = self.get_response(connector, path, attr, response, fresh_api_key, **kwargs)

        # save response to cache to make it faster
        self.save_cache(path_url.name(), response, **self.cache_expired_datetime)

        return response


    def enable_auto_cleanup(self, status=True):
        """Enable or disable automatic cache cleanup"""
        self.auto_cleanup_cache = status


    def cleanup_expired_cache(self):
        """Manually cleanup expired cache entries"""
        if hasattr(self, 'caching_system') and self.caching_system:
            return super().cleanup_expired_cache()
        return {'expired_count': 0, 'removed_files': [], 'remaining_cache': 0}


    def get_cache_stats(self):
        """Get cache statistics"""
        if hasattr(self, 'caching_system') and self.caching_system:
            return super().get_cache_stats()
        return {'total_cache_entries': 0, 'total_size_bytes': 0, 'total_size_mb': 0}


    def clear_all_cache(self):
        """Clear all cache entries"""
        if hasattr(self, 'caching_system') and self.caching_system:
            return super().clear_all_cache()
        return {'removed_files': 0, 'cleared_database': False}


    def delete_cache_by_path(self, path):
        """Delete specific cache by path"""
        if hasattr(self, 'caching_system') and self.caching_system:
            return super().delete_cache_by_path(path)
        return False
    
