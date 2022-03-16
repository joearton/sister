import requests
import json
import os
import validators
from settings import *


class PathURL:

    def __init__(self, path_url, path):
        self.path_url = path_url
        self.path = path
    
    def __str__(self):
        return self.path_url

    def name(self):
        return self.path


class SisterIO:

    def read_file(self, filename):
        obj = {}
        if os.path.isfile(filename):
            with open(filename, 'r') as reader:
                obj = json.loads(reader.read())
        return obj


    def update_file(self, filename, filepath, **kwargs):
        for key, value in kwargs.items():
            filepath[key] = str(value)
        with open(filename, 'w') as writer:
            writer.write(json.dumps(filepath, indent=4))
        return self.read_file(filename)


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
        if not validators.url(self.config['sister_url']):
            print(f"{self.config['sister_url']} is not valid URL")
            return False
        try:
            r = requests.get(self.config['sister_url'], timeout=3)
        except:
            print(f"{self.config['sister_url']} cant't be reached, check your URL")
            return False
        return True


    def get_ws_url(self):
        ws_root_url = self.config['sister_url']
        if ws_root_url.endswith('/'):
            ws_root_url = self.config['sister_url'][:-1]
        ws_url = self.spec.get_server('sandbox')['url']
        if not self.config['use_sandbox']:
            ws_url = self.spec.get_server('ws')['url']
        return f'{ws_root_url}{ws_url}'


    def parse_path_url(self, path, **query):
        # get more info about query here
        # so we can take more
        counter, params = 0, {}
        if '__params__' in query:
            __params__ = query.get('__params__')
            for param in __params__:
                name = param.get('name')
                if name: params[name] = param

        # filter query, only accept public kwargs
        fil_query = dict(filter(lambda x: not x[0].startswith('__') and not x[0].endswith('__'), query.items()))
        for key, value in fil_query.items():
            param   = params.get(key)
            in_type = 'query'
            if param:
                in_type = param.get('in')
            if in_type == 'path':
                path = path.replace('{{{key}}}'.format(key=key), value)
            else:
                path += '?' if counter == 0 else '&'
                path += f'{key}={value}'
                counter += 1
        path_url = f"{self.get_ws_url()}{path}"
        return PathURL(path_url, path)
