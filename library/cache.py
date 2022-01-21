from asyncore import write
from linecache import cache
from library.template import SisterTemplate
import json, os
from settings import *
import uuid 


class AttrDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__



class CacheAsJson:

    def __init__(self):
        self.cache_db_filename = os.path.join(CACHE_DIR,  'cache_db.json')


    def get_unique_id(self, length=15):
        unique_id = uuid.uuid4()
        unique_id = unique_id.hex[:length].upper()
        return unique_id


    def read_db(self, cache_id: str = ''):
        db_object = {}
        # check saved db object
        if os.path.isfile(self.cache_db_filename):
            with open(self.cache_db_filename, 'r') as reader:
                db_object = json.load(reader)
        if cache_id and db_object:
            cache_object = db_object.get(cache_id)
            if cache_object:
                return cache_object
        else:     
            return db_object


    def get_item(self, id):
        return self.read_db(id)


    def is_exist(self, id):
        return len(self.read_db(id)) > 0


    def write_db(self, cache_object):
        cache_id = cache_object['id']
        saved_db_object = self.read_db()
        saved_db_object[cache_id] = cache_object
        with open(self.cache_db_filename, 'w') as writer:
            json.dump(saved_db_object, writer)


    def save(self, cache_object: dict):
        self.write_db(cache_object)


    def get(self, cache_id):
        cache_object = self.read_db(cache_id)
        return cache_object


    def delete(self, cache_id):
        db_object = self.read_db()
        deleted_object = {}
        if cache_id in db_object:
            deleted_object = db_object[cache_id]
            db_object.pop(cache_id, None)
            with open(self.cache_db_filename, 'w') as writer:
                json.dump(db_object, writer)
        return deleted_object


class SisterCache(SisterTemplate):

    def __init__(self, cache_db_class = CacheAsJson):
        self.cache_db_class = cache_db_class()
        self.cache_ext = 'json'


    def path_as_io(self, path):
        path_name = path.replace('/', '_')
        if path_name.startswith('_'):
            path_name = path_name[1:]
        return path_name


    def get_cache_fname(self):
        unique_id = self.cache_db_class.get_unique_id()
        if unique_id in os.listdir(CACHE_DIR):
            return self.get_cache_fname() 
        cache_fname = f'{unique_id}.{self.cache_ext}'
        return cache_fname


    def get_cache_fpath(self):
        cache_fpath = os.path.join(CACHE_DIR, self.get_cache_fname())
        return cache_fpath


    def read_cache_file(self, cache_object):
        json_object = {}
        filepath = cache_object['filepath']
        if os.path.isfile(filepath):
            with open(filepath, 'r') as reader:
                json_object = json.load(reader)
        else:
            self.cache_db_class.delete(cache_object['id'])
        return json_object


    def write_cache_file(self, path, response):
        cache_fpath = self.get_cache_fpath()
        with open(cache_fpath, 'w') as writer:
            json.dump(response['data'], writer)
        return [path, cache_fpath, response]


    def remove_cache_file(self, filepath):
        if os.path.isfile(filepath):
            os.remove(filepath)


    def get_object(self, path, filepath, response):
        cache_object = {
            'id': self.path_as_io(path),
            'path': path, # ws path, not directory
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'accessed_at': self.get_iso_datetime(),
            'length': len(response['data']),
        }
        return cache_object


    def save_cache(self, path, response):
        if not response['status'] == True:
            return None
        # write and update cache database
        cache_object = self.write_cache_file(path, response)
        cache_object = self.get_object(*cache_object)
        self.cache_db_class.save(cache_object)


    def get_cache(self, path):
        if self.caching_system is False:
            return None
        cache_id = self.path_as_io(path)
        cache_object = self.cache_db_class.get(cache_id)
        if cache_object:
            cache_object['data'] = self.read_cache_file(cache_object)
        return cache_object

