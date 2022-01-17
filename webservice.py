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


def to_json(text):
    json_object = json.loads(text)
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
                obj = to_json(reader.read())
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
        token = ""
        get_token = self.session.post("{0}/authorize".format(
            self.config['sister_url']), json=auth_data, headers=headers)
        if get_token.status_code == 200:
            json_object = get_token.json()
            if "token" in json_object:
                token = json_object['token']
                self.update_api_key(token=token, last_request='')
        return token


    def get_data(self, scope, **kwargs):
        response = {
            'status'    : 'error',
            'message'   : 'Error occured',
            'detail'    : '',
            'data'      : {},
        }
        scope_url = "{0}/{1}".format(self.config['sister_url'], scope)
        counter   = 0
        for key, value in kwargs.items():
            if counter == 0:
                scope_url += '?'
            else:
                scope_url += '&'
            scope_url += f'{key}={value}'
            counter += 1
        # when request is to get all data
        result = self.session.get(scope_url, auth=BearerAuth(self.api_key['token']))
        if to_json(result.text):
            json_object = result.json()
            if result.status_code in [200, 204]:
                response['status'] = True
                response['message'] = 'Success executed'
                response['data'] = json_object
            elif result.status_code in ['401']:
                self.request_api_key()
                self.get_data(scope, kwargs)
            else:
                if json_object['message']:
                    response['message'] = json_object['message']
                    response['detail'] = json_object['detail']
        return response



api  = SisterAPI()
data = api.get_data('referensi/sdm')
print(data['data'])