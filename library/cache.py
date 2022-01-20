from library.template import SisterTemplate
import json, os
from settings import *


CACHE_DB_FILENAME = os.path.join(CACHE_DIR,  'cache_db.json')


class SisterCache(SisterTemplate):

    def path_as_io(self, path):
        path_name = path.replace('/', '_')
        if path_name.startswith('_'):
            path_name = path_name[1:]
        return path_name


    def get_cache_fname(self, path, ext='json'):
        cache_fname = f'{self.path_as_io(path)}.{ext}'
        return cache_fname


    def get_cache_fpath(self, path, ext='json'):
        cache_fpath = os.path.join(CACHE_DIR, self.get_cache_fname(path, ext))
        return cache_fpath


    def write_cache_object(self, path, response):
        json_object = json.dumps({
            'accessed_at': self.get_iso_datetime(),
            'data': response['data'],
            'length': len(response['data']),
        })
        cache_fpath = self.get_cache_fpath(path)
        with open(cache_fpath, 'w') as writer:
            writer.write(json_object)
        return json_object


    def read_cache_object(self, path):
        json_object = {}
        cache_fpath = self.get_cache_fpath(path)
        if os.path.isfile(cache_fpath):
            with open(cache_fpath, 'r') as reader:
                json_object = json.load(reader)
        return json_object



    def save_to_cache(self, path, response):
        if not response['status'] == True:
            return None
        # write and update cache database
        self.write_cache_object(path, response)
            

    def get_from_cache(self, path):
        if self.caching_system == True:
            return self.read_cache_object(path)
