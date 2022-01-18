from asyncore import read
import yaml
import os
from library.settings import *


API_SPEC_FILE = os.path.join(CONFIG_DIR, 'api_spec.yaml')


class BaseSpec:

    def initialization(self):
        self.api_spec = self.get_specs()


    def get_specs(self):
        spec = None
        with open(API_SPEC_FILE, 'r') as reader:
            spec = yaml.safe_load(reader)
        return spec


    def get_spec(self, name):
        if name in self.get_spec_root():
            return self.api_spec.get(name)


    def get_spec_root(self):
        return list(self.api_spec.keys())



class SisterSpec(BaseSpec):

    def get_openapi(self) -> str:
        return self.get_spec('openapi')


    def get_info(self) -> dict:
        return self.get_spec('info')


    def get_servers(self) -> list:
        return self.get_spec('servers')


    def get_server(self, server_name) -> dict:
        servers = self.get_servers()
        servers = filter(lambda x: x['url'].find(server_name.lower()) != -1, servers)
        server = list(servers)
        return server[0]


    def get_tags(self) -> list:
        return self.get_spec('tags')


    def get_tag(self, tag_name) -> list:
        tags = self.get_tags()
        tags = filter(lambda x: x['name'].lower() == tag_name.lower(), tags)
        tag  = list(tags)[0]
        return tag


    def get_paths(self) -> list:
        return self.get_spec('paths')


    def get_path(self, path_name) -> tuple:
        paths = self.get_paths()
        paths = filter(lambda x: x[0] == path_name, paths.items())
        path  = None
        if paths:
            path = list(paths)[0]
        return path


    def get_path_method_and_attr(self, path_name):
        path_name, path_attr   = self.get_path(path_name)
        path_method, path_attr = [[method, attr] for method, attr in path_attr.items()][0]
        return (path_method, path_attr)


    def get_components(self) -> list:
        return self.get_spec('components')


    def get_component(self, component_name) -> list:
        components = self.get_spec('components')
        components = filter(lambda x: x[0] == component_name, components.items())
        component  = list(components)[0]
        return component