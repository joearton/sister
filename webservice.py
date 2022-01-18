import requests
import json
import os
from datetime import datetime, timedelta 


BASE_DIR     = os.getcwd()
CACHE_DIR    = os.path.join(BASE_DIR, '.cache')
CONFIG_FILE  = os.path.join(BASE_DIR, 'config.json')
API_KEY_FILE = os.path.join(CACHE_DIR, 'api_key.json')


if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


if not os.path.isfile(CONFIG_FILE):
    print('Config file available, create it in '. CONFIG_FILE)
    os.abort()


def is_json(text):
    try:
        json_object = json.load(text)
    except:
        json_object = None
    return json_object


class BearerAuth(requests.auth.AuthBase):
    '''
        used to provide token bearer
    '''

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = "Accept: application/json"
        r.headers["Authorization"] = "Bearer " + self.token
        return r



class SisterIO:

    def read_file(self, filename):
        obj = {}
        if os.path.isfile(filename):
            with open(filename, 'r') as reader:
                obj = json.loads(reader.read())
        return obj


    def update_file(self, filename, filescope, **kwargs):
        for key, value in kwargs.items():
            filescope[key] = value
        with open(filename, 'w') as writer:
            writer.write(json.dumps(filescope))
        return self.read_file(filename)



class SisterAPI(SisterIO):

    def __init__(self):
        self.session = requests.session()
        self.config  = self.read_config()
        self.api_key = self.read_api_key()
        self.check_config()


    def read_config(self):
        return self.read_file(CONFIG_FILE)


    def update_config(self, **kwargs):
        config = self.update_file(CONFIG_FILE, self.config, **kwargs)
        self.config = config


    def read_api_key(self):
        return self.read_file(API_KEY_FILE)


    def update_api_key(self, **kwargs):
        api_key = self.update_file(API_KEY_FILE, self.api_key, **kwargs)
        self.api_key = api_key


    def check_config(self):
        # check sister URL for 7 seconds
        try:
            response = self.session.get(self.get_ws_url(), timeout=7)
        except requests.exceptions.ConnectionError:
            raise requests.exceptions.ConnectionError('Connection error, Check your Sister URL')
        try:
            response = self.session.get(self.get_ws_url(), timeout=7)
        except requests.exceptions.ConnectTimeout:
            raise requests.exceptions.ConnectTimeout('Connection error, Check your Sister URL')



    def get_ws_url(self):
        ws_url = self.config['sister_url']
        ws_version = self.config['api_version']
        if self.config['use_sandbox']:
            return f'{ws_url}/ws.php/{ws_version}'
        return f'{ws_url}/ws-sandbox.php/{ws_version}'


    def request_api_key(self):
        auth_data = {
            "username"      : self.config['username'],
            "password"      : self.config['password'],
            "id_pengguna"   : self.config['id_pengguna']
        }
        headers  = {
            "Accept"        : "application/json",
            "Content-Type"  : "application/json"
        }
        api_key = self.session.post("{0}/authorize".format(
            self.get_ws_url()), json=auth_data, headers=headers)
        if api_key.status_code == 200:
            if is_json(api_key):
                api_key = api_key.json()
                if "token" in api_key:
                    self.update_api_key(token=api_key['token'], last_request='')
            else:
                api_key = self.get_res_template()
        return api_key


    def get_res_template(self):
        response = {
            'status'    : 'error',
            'message'   : 'Error occured',
            'detail'    : '',
            'data'      : {},
        }
        return response
        

    def parse_scope_url(self, scope, query):
        scope_url = f"{self.get_ws_url()}/{scope}"
        counter   = 0
        for key, value in query.items():
            if counter == 0:
                scope_url += '?'
            else:
                scope_url += '&'
            scope_url += f'{key}={value}'
            counter += 1
        return scope_url


    def get_data(self, scope, **kwargs):
        response = self.get_res_template()
        if not self.api_key:
            return response
        scope_url = self.parse_scope_url(scope, kwargs)
        result = self.session.get(scope_url, auth=BearerAuth(self.api_key['token']))
        if is_json(result.text):
            json_object = result.json()
            if 'message' in json_object:
                if result.status_code in ['401']:
                    self.request_api_key()
                response['message'] = json_object['message']
                response['detail'] = json_object['detail']
            else:
                response['status'] = True
                response['message'] = 'Success executed'
                response['data'] = json_object
        return response



api  = SisterAPI()
data = api.get_data('referensi/sdm')
print(data)