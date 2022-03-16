import json
from datetime import datetime, timedelta
from subprocess import call 


class Response(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


class SisterTemplate:

    def set_cache_expired_day(self, day):
        self.cache_expired_day = day

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
        return Response(response)


    def iso_to_datetime(self, iso_datetime):
        iso_format = "%Y-%m-%d %H:%M:%S.%f"
        dt_format  = datetime.strptime(iso_datetime, iso_format)
        return dt_format


    def get_now_datetime(self, isoformat=False):
        # created for json dumps 
        current_datetime = datetime.now()
        if isoformat:
            current_datetime.isoformat()
        return current_datetime

    
    def get_expired_datetime(self, old_datetime=None, isoformat=False, **expired_set):
        if old_datetime:
            expired_datetime = timedelta(**expired_set) + old_datetime
        expired_datetime = timedelta(**expired_set) + self.get_now_datetime()
        if isoformat:
            expired_datetime.isoformat()
        return expired_datetime
