import json

from debugpy import connect
from library.connector import SisterSession, BearerAuth
from library.io import SisterIO
from library.api_spec import SisterSpec
from library.settings import *


class SisterTemplate:

    def response_template(self):
        response = {
            'status'    : False,
            'message'   : 'Error occured',
            'detail'    : '',
            'data'      : {},
        }
        return response


    def api_key_template(self):
        return {
            'token'         : '',
            'last_request'  : ''
        }


    def get_auth_data(self):
        auth_data = {
            "username"      : self.config['username'],
            "password"      : self.config['password'],
            "id_pengguna"   : self.config['id_pengguna']
        }
        return auth_data


    def is_json(self, text):
        try:
            json_object = json.loads(text)
        except:
            json_object = {}
        return json_object


    def parse_response(self, response, as_json=False):
        if response['data']:
            response['status']  = True
            response['message'] = ''
        if as_json:
            response = json.dumps(response, indent=4)
        return response



class SisterAPI(SisterIO, SisterTemplate):

    def __init__(self):
        self.session = SisterSession()
        self.config  = self.read_config()
        self.api_key = self.read_api_key()
        self.valid_config = self.check_config()
        self.spec = SisterSpec()
        self.spec.initialization()


    def request_api_key(self):
        response = self.response_template()
        if not self.valid_config:
            response['message'] = 'Config or API is not valid'
            return self.parse_response(response)
        auth_data   = self.get_auth_data()
        get_api_key = self.session.post(f"{self.get_ws_url()}/authorize", json=auth_data)
        if self.is_json(get_api_key.text):
            json_api_key = get_api_key.json()
            if get_api_key.status_code == STATUS_SUCCESS:
                self.update_api_key(token=json_api_key['token'], role=json_api_key['role'], last_request='')
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
            

    def get_data(self, path, fresh_api_key, **kwargs):
        response = self.response_template()
        # check whether the config is valid or not
        if not self.valid_config:
            response['message'] = 'Config or API is not valid'
            return response
        # check whether authorization is success or not
        if not self.api_key:
            api_key = self.request_api_key()
            if not api_key['status'] == True:
                return api_key
            # get fresh api key
            self.api_key = self.read_api_key()

        method, attr = self.spec.get_path_method_and_attr(path)
        path_url  = self.parse_path_url(path, kwargs)
        connector = self.connect(method, path_url)
        response  = self.get_response(connector, path, response, fresh_api_key, **kwargs)        
        return response
    

api = SisterAPI()
res = api.get_data('/referensi/sdm', False, nidn="0219128601")
res = res['data'][0]
id_sdm = res['id_sdm']

print(id_sdm)