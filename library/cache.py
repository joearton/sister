from library.template import SisterTemplate
import json, os
from settings import *


CACHE_DB_FILENAME = os.path.join(CACHE_DIR,  'cache_db.json')


class SisterCache(SisterTemplate):

    def path_as_io(self, path):
        return path.replace('/', '_')


    def write_cache_object(self, path, response):
        path_name = self.path_as_io(path)
        cache_filename = os.path.join(CACHE_DIR, f"{path_name}.json")
        json_data = json.dumps(response['data'])
        with open(cache_filename, 'w') as writer:
            writer.write(json_data)
        return (cache_filename, json_data)


    def read_cache_object(self, path):
        json_object = {}
        path_name = self.path_as_io(path)
        cache_obj = self.read_cache_db(path_name)
        if cache_obj:
            if os.path.isfile(cache_obj['filename']):
                with open(cache_obj['filename'], 'r') as reader:
                    json_object = json.load(reader)
        return json_object


    def read_cache_db(self, path_name=None):
        data = {}
        if os.path.isfile(CACHE_DB_FILENAME):
            with open(CACHE_DB_FILENAME, 'r') as reader:
                data = json.load(reader)
        if path_name in data:
            return data[path_name]
        return data


    def save_to_cache(self, path, response):
        if not response['status'] == True:
            return None
        # write and update cache database
        (cache_filename, json_data) = self.write_cache_object(path, response)
        path_name = self.path_as_io(path)
        cache_db  = self.read_cache_db()
        cache_db[path_name] = {
            'basename': os.path.basename(cache_filename),
            'filename': cache_filename,
            'last_access': self.get_iso_datetime(),
            'length': len(json_data)
        }
        with open(CACHE_DB_FILENAME, 'w') as writer:
            json.dump(cache_db, writer)
            

    def get_from_cache(self, path):
        if self.caching_system == True:
            return self.read_cache_object(path)
