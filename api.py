import inspect
import re
from functools import partial
from library.webservice import WebService


class WsSisterAPI(WebService):

    def __init__(self):
        super().__init__()
        self.reply_as_json = False
        # create automatic function from sister api spec
        # for example, get /referensi/sdm
        # you can call /referensi/sdm using below code
        # api = SisterApi()
        # res = api.get_referensi_sdm()
        # note that / in path become _ in function
        self.create_func_from_spec()


    def create_func_from_spec(self):
        self.paths = self.spec.get_paths()
        for path in self.paths:
            isb_format  = r"[/]{([^{}]+)}" # inside curly bracket
            func_name   = re.sub(r"\/", '_', path)
            url_paths   = re.findall(isb_format, path)
            for url_path in url_paths:
                func_name = func_name.replace(f'{{{url_path}}}', 'bypath')
            # remove _ in first func_name
            if func_name.startswith('_'):
                func_name = func_name[1:]
            self.add_get_function(f'get_{func_name}', path)


    def add_to_class(self, name, content):
        if not inspect.isclass(content) and hasattr(content, 'class_contribute'):
            content.class_contribute(self, name)
        else:
            setattr(self, name, content)


    def check_required_param(self, path):
        params = self.spec.get_path_params(path)        
        required_params = list(filter(lambda x: x.get('required') == True, params))
        required_params = [x['name'] for x in required_params]
        return [required_params, params]


    def master_get_function(self, path, **kwargs):
        required_params, params = self.check_required_param(path)
        for param_name in required_params:
            if not param_name in kwargs:
                raise NameError(f'Require argument {list(required_params)}\n\nARGUMENTS HINT:\n{params}')
        # put more accessible info about params
        kwargs['__params__'] = params
        res = self.get_data(path, **kwargs)
        return self.parse_response(res, as_json=self.reply_as_json)


    def add_get_function(self, name, path, **kwargs):
        self.add_to_class(name, partial(self.master_get_function, path, **kwargs))


SisterAPI = WsSisterAPI()