import requests
import json
import os
import validators
from library.settings import *
from datetime import datetime, timedelta 


class SisterIO:

    def read_file(self, filename):
        obj = {}
        if os.path.isfile(filename):
            with open(filename, 'r') as reader:
                obj = json.loads(reader.read())
        return obj


    def update_file(self, filename, filepath, **kwargs):
        for key, value in kwargs.items():
            filepath[key] = value
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
        ws_url = self.spec.get_server('sandbox')['url']
        if not self.config['use_sandbox']:
            ws_url = self.spec.get_server('ws')['url']
        return f'{ws_root_url}{ws_url}'


    def parse_path_url(self, path, query):
        path_url = f"{self.get_ws_url()}{path}"
        counter   = 0
        for key, value in query.items():
            if counter == 0:
                path_url += '?'
            else:
                path_url += '&'
            path_url += f'{key}={value}'
            counter += 1
        return path_url
