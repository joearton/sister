import json

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