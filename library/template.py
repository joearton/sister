import json
from datetime import datetime 


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
            'accessed_at'  : ''
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


    def get_iso_datetime(self):
        # created for json dumps 
        now = datetime.now()
        iso = now.isoformat()
        return iso


    def get_now_datetime(self):
        # created for json dumps 
        now = datetime.now()
        return now


    def iso_to_datetime(self, iso_datetime):
        iso_format = "%Y-%m-%dT%H:%M:%S.%f"
        dt_format  = datetime.strptime(iso_datetime, iso_format)
        return dt_format

    
    def get_rest_datetime(self, old_datetime):
        return (self.get_now_datetime() - self.iso_to_datetime(old_datetime))

