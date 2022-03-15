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
        self.api_key = self.read_api_key()
        self.caching_system = True
        self.token_expired_time = 60*60 # one hour
        self.caching_expired_time = 60*60*24 # one hour


    def use_cache(self, status=True):
        self.caching_system = status


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
                self.update_api_key(token=json_api_key['token'],
                    role=json_api_key['role'], accessed_at=self.get_iso_datetime())
                response['data'] = json_api_key
            else:
                response['message'] = json_api_key['message']
                response['detail'] = json_api_key['detail']
        else:
            response['message'] = "Response is not in JSON format, check your URL"
        return self.parse_response(response)
        

    def get_response(self, connector, path, attr, response, fresh_api_key, **kwargs):
        content_type = connector.headers.get('Content-Type')
        if content_type == 'application/json':
            json_object = connector.json()
            if connector.status_code in [STATUS_SUCCESS, STATUS_SUCCESS_NO_REPLY]:
                response['data'] = json_object
            elif connector.status_code in [STATUS_TOKEN_INVALID]:
                if fresh_api_key:
                    response['message'] = "API key invalid, check your credential"
                    return self.parse_response(response)
                self.request_api_key()
                self.get_data(path, True, **kwargs)
            else:
                response['message'] = json_object['message']
                response['detail']  = json_object['detail']
        else:
            response['message'] = "Response is not in JSON format"
            # if response is byte/binnary like image
            response['data'] = connector.content
            response['content-type'] = content_type
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
        response = self.response_template()
        path_url = self.parse_path_url(path, **kwargs)

        # check whether authorization is success or not
        if not self.api_key:
            api_key = self.request_api_key()
            if not api_key['status'] == True:
                return api_key        
            self.api_key = self.read_api_key()

        # check from cache
        cache_available = self.get_cache(path_url.name())
        if cache_available:
            response['data'] = cache_available['data']
            rest_time = self.get_rest_datetime(cache_available.get('accessed_at'))
            if rest_time.total_seconds() <= self.caching_expired_time:
                return response

        # check api-key expiration
        if self.api_key.get('accessed_at'):
            rest_time = self.get_rest_datetime(self.api_key.get('accessed_at'))
            if rest_time.total_seconds() >= self.token_expired_time:
                self.request_api_key()

        self.api_key = self.read_api_key()
        method, attr = self.spec.get_path_method_and_attr(path)
        connector = self.connect(method, path_url)
        response  = self.get_response(connector, path, attr, response, fresh_api_key, **kwargs)

        # save response to cache to make it faster
        self.save_cache(path_url.name(), response)

        return response
    
