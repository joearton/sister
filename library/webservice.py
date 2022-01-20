import json
from library.connector import SisterSession, BearerAuth
from library.io import SisterIO
from library.api_spec import SisterSpec
from library.cache import SisterCache
from settings import *



class WebService(SisterIO, SisterCache):

    def __init__(self):
        self.session = SisterSession()
        self.config  = self.read_config()
        self.api_key = self.read_api_key()
        self.caching_system = True
        self.token_expired_time = 60*60 # one hour
        self.caching_expired_time = 60*60*24 # one hour
        self.spec = SisterSpec()


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
                    role=json_api_key['role'], last_request=self.get_iso_datetime())
                response['data'] = json_api_key
            else:
                response['message'] = json_api_key['message']
                response['detail'] = json_api_key['detail']
        else:
            response['message'] = "Response is not in JSON format, check your URL"
        return self.parse_response(response)
        

    def get_response(self, connector, path, response, fresh_api_key, **kwargs):
        if self.is_json(connector.text):
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
            response['message'] = "Response is not in JSON format, check your URL"
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
        response = connector(path_url, auth=BearerAuth(self.api_key['token']))
        return response
            


    def get_data(self, path, fresh_api_key=False, **kwargs):
        response = self.response_template()
        # check whether authorization is success or not
        if not self.api_key:
            api_key = self.request_api_key()
            if not api_key['status'] == True:
                return api_key        

        cache_available = self.get_from_cache(path)
        if cache_available:
            response['data'] = cache_available
            return response

        rest_time = self.get_rest_datetime(self.api_key['last_request'])
        if rest_time.total_seconds() >= self.token_expired_time:
            self.request_api_key()

        self.api_key = self.read_api_key()
        method, attr = self.spec.get_path_method_and_attr(path)
        path_url  = self.parse_path_url(path, kwargs)
        connector = self.connect(method, path_url)
        response  = self.get_response(connector, path, response, fresh_api_key, **kwargs)
        self.save_to_cache(path, response)
        return response
    
