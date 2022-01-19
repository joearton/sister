import inspect
import re
from functools import partial
from library.webservice import WebService


class SisterAPI(WebService):

    def __init__(self):
        super().__init__()
        self.reply_as_json = False
        self.paths = self.spec.get_paths()
        # create automatic function from sister api spec
        # for example, get /referensi/sdm
        # you can call /referensi/sdm using below code
        # api = SisterApi()
        # res = api.get_referensi_sdm()
        # note that / in path become _ in function
        for path in self.paths:
            func_name = re.sub(r"\/", '_', re.sub(r"[/]{([^{}]+)}", '', path))
            params = self.spec.get_path_params(path)
            kwargs = {}
            for param_dict in params:
                if param_dict.get('in'):
                    kwargs[param_dict.get('name')] = {'required': param_dict.get('required'), 'value': ''}
            self.add_get_function(f'get{func_name}', path, **kwargs)


    def add_to_class(self, name, content):
        if not inspect.isclass(content) and hasattr(content, 'class_contribute'):
            content.class_contribute(self, name)
        else:
            setattr(self, name, content)


    def master_get_function(self, path, **kwargs):
        parsed_kwargs = {}
        for key, value in kwargs.items():
            if value.get('required') and len(value.get('value')) == 0:
                raise NameError(f'Require argument {list(kwargs.keys())}\n\nARGUMENTS HINT: {self.spec.get_path_params(path)}')
            else:
                parsed_kwargs[key] = value['value']
        res = self.get_data(path, **parsed_kwargs)
        return self.parse_response(res, as_json=self.reply_as_json)


    def add_get_function(self, name, path, **kwargs):
        self.add_to_class(name, partial(self.master_get_function, path, **kwargs))

