from library.template import SisterTemplate
from settings import *
import json, os, re
import uuid 
import threading
import fcntl


class AttrDict(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__



class CacheAsJson:

    def __init__(self):
        self.cache_db_filename = os.path.join(CACHE_DIR,  'cache_db.json')
        self._lock = threading.Lock()


    def get_unique_id(self, length=15):
        unique_id = uuid.uuid4()
        unique_id = unique_id.hex[:length].upper()
        return unique_id


    def read_db(self, cache_id: str = ''):
        db_object = {}
        # check saved db object
        if os.path.isfile(self.cache_db_filename):
            try:
                with open(self.cache_db_filename, 'r') as reader:
                    fcntl.flock(reader.fileno(), fcntl.LOCK_SH)  # Shared lock for reading
                    try:
                        db_object = json.load(reader)
                    finally:
                        fcntl.flock(reader.fileno(), fcntl.LOCK_UN)  # Release lock
            except json.decoder.JSONDecodeError:
                os.remove(self.cache_db_filename)
            except Exception as e:
                print(f"Error reading cache file: {e}")
        if cache_id and db_object:
            cache_object = db_object.get(cache_id)
            if cache_object:
                return cache_object
        else:     
            return db_object


    def get_item(self, id):
        # alias for read_db with cache_id
        return self.read_db(id)


    def is_exist(self, id):
        return len(self.read_db(id)) > 0


    def write_db(self, cache_object):
        cache_id = cache_object['id']
        saved_db_object = self.read_db()
        saved_db_object[cache_id] = cache_object
        try:
            with open(self.cache_db_filename, 'w') as writer:
                fcntl.flock(writer.fileno(), fcntl.LOCK_EX)  # Exclusive lock for writing
                try:
                    json.dump(saved_db_object, writer)
                finally:
                    fcntl.flock(writer.fileno(), fcntl.LOCK_UN)  # Release lock
        except Exception as e:
            print(f"Error writing cache file: {e}")


    def save(self, cache_object: dict):
        self.write_db(cache_object)


    def get(self, cache_id):
        cache_object = self.read_db(cache_id)
        if not cache_object:
            cache_object = {}
        return cache_object


    def delete(self, cache_id):
        db_object = self.read_db()
        deleted_object = {}
        if cache_id in db_object:
            deleted_object = db_object[cache_id]
            db_object.pop(cache_id, None)
            try:
                with open(self.cache_db_filename, 'w') as writer:
                    fcntl.flock(writer.fileno(), fcntl.LOCK_EX)  # Exclusive lock for writing
                    try:
                        json.dump(db_object, writer)
                    finally:
                        fcntl.flock(writer.fileno(), fcntl.LOCK_UN)  # Release lock
            except Exception as e:
                print(f"Error deleting cache item: {e}")
        return deleted_object


    def get_all_cache_ids(self):
        """Get all cache IDs from database"""
        db_object = self.read_db()
        return list(db_object.keys())


    def cleanup_expired_cache(self, cache_manager):
        """Remove all expired cache entries"""
        db_object = self.read_db()
        expired_count = 0
        removed_files = []
        
        for cache_id, cache_object in list(db_object.items()):
            try:
                # Check if cache is expired
                expired_at = cache_object.get('expired_at')
                if expired_at:
                    expired_datetime = cache_manager.iso_to_datetime(expired_at)
                    current_datetime = cache_manager.get_now_datetime()
                    
                    if current_datetime > expired_datetime:
                        # Cache is expired, remove it
                        filepath = cache_object.get('filepath')
                        if filepath and os.path.isfile(filepath):
                            try:
                                os.remove(filepath)
                                removed_files.append(filepath)
                            except OSError as e:
                                print(f"Error removing cache file {filepath}: {e}")
                        
                        # Remove from database
                        db_object.pop(cache_id, None)
                        expired_count += 1
                        
            except Exception as e:
                print(f"Error checking cache expiration for {cache_id}: {e}")
                # Remove corrupted cache entry
                db_object.pop(cache_id, None)
                expired_count += 1
        
        # Save updated database
        if expired_count > 0:
            try:
                with open(self.cache_db_filename, 'w') as writer:
                    fcntl.flock(writer.fileno(), fcntl.LOCK_EX)
                    try:
                        json.dump(db_object, writer)
                    finally:
                        fcntl.flock(writer.fileno(), fcntl.LOCK_UN)
            except Exception as e:
                print(f"Error saving cache database after cleanup: {e}")
        
        return {
            'expired_count': expired_count,
            'removed_files': removed_files,
            'remaining_cache': len(db_object)
        }


    def get_cache_stats(self):
        """Get cache statistics"""
        db_object = self.read_db()
        total_cache = len(db_object)
        total_size = 0
        expired_count = 0
        
        for cache_id, cache_object in db_object.items():
            filepath = cache_object.get('filepath')
            if filepath and os.path.isfile(filepath):
                try:
                    total_size += os.path.getsize(filepath)
                except OSError:
                    pass
        
        return {
            'total_cache_entries': total_cache,
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2)
        }



class SisterCache(SisterTemplate):

    def __init__(self, cache_db_class=CacheAsJson):
        self.cache_db_class = cache_db_class()
        self.cache_ext = 'json'


    def path_as_io(self, path):
        path_name = re.sub(r"[/ ]", "-", path)
        path_name = path_name.lower()
        if path_name.startswith('-'):
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
            try:
                with open(filepath, 'r') as reader:
                    json_object = json.load(reader)
            except json.decoder.JSONDecodeError:
                os.remove(filepath)
                self.cache_db_class.delete(cache_object['id'])
        else:
            self.cache_db_class.delete(cache_object['id'])
        return json_object


    def write_cache_file(self, path, response, cache_fpath=None):
        if not cache_fpath:
            cache_fpath = self.get_cache_fpath()
        try:
            with open(cache_fpath, 'w') as writer:
                json.dump(response['data'], writer)
            return [path, cache_fpath, response]
        except TypeError: # because it might be byte or binnary
            return False


    def remove_cache_file(self, filepath):
        if os.path.isfile(filepath):
            os.remove(filepath)


    def get_object(self, path, filepath, response):
        cache_object = {
            'id': self.path_as_io(path),
            'path': path, # ws path, not directory
            'filename': os.path.basename(filepath),
            'filepath': filepath,
            'accessed_at': str(self.get_now_datetime(isoformat=True)),
            'expired_at': str(self.get_expired_datetime(isoformat=True, **self.cache_expired_datetime)),
            'length': len(response['data']),
        }
        return cache_object


    def save_cache(self, path, response, **cache_expired_datetime):
        self.cache_expired_datetime = cache_expired_datetime
        if not response['status'] == True:
            return None
        
        # check whether cache is exists or not
        cache_fpath = None
        cache_id    = self.path_as_io(path)
        saved_cache = self.cache_db_class.get_item(cache_id)
        if saved_cache:
            cache_fpath = saved_cache.get('filepath')

        # write cache object to file
        cache_object = self.write_cache_file(path, response, cache_fpath)
        if cache_object:
            cache_object = self.get_object(*cache_object)
            self.cache_db_class.save(cache_object)


    def get_cache(self, path):
        cache_object = {}
        if self.caching_system:
            cache_id = self.path_as_io(path)
            cache_object = self.cache_db_class.get(cache_id)
            if cache_object:
                cache_object['data'] = self.read_cache_file(cache_object)
        return cache_object


    def cleanup_expired_cache(self):
        """Remove all expired cache entries"""
        return self.cache_db_class.cleanup_expired_cache(self)


    def get_cache_stats(self):
        """Get cache statistics"""
        return self.cache_db_class.get_cache_stats()


    def clear_all_cache(self):
        """Clear all cache entries"""
        db_object = self.cache_db_class.read_db()
        removed_count = 0
        
        for cache_id, cache_object in db_object.items():
            filepath = cache_object.get('filepath')
            if filepath and os.path.isfile(filepath):
                try:
                    os.remove(filepath)
                    removed_count += 1
                except OSError as e:
                    print(f"Error removing cache file {filepath}: {e}")
        
        # Clear database
        try:
            with open(self.cache_db_class.cache_db_filename, 'w') as writer:
                fcntl.flock(writer.fileno(), fcntl.LOCK_EX)
                try:
                    json.dump({}, writer)
                finally:
                    fcntl.flock(writer.fileno(), fcntl.LOCK_UN)
        except Exception as e:
            print(f"Error clearing cache database: {e}")
        
        return {
            'removed_files': removed_count,
            'cleared_database': True
        }


    def delete_cache_by_path(self, path):
        """Delete specific cache by path"""
        cache_id = self.path_as_io(path)
        cache_object = self.cache_db_class.get(cache_id)
        
        if cache_object:
            filepath = cache_object.get('filepath')
            if filepath and os.path.isfile(filepath):
                try:
                    os.remove(filepath)
                except OSError as e:
                    print(f"Error removing cache file {filepath}: {e}")
            
            # Remove from database
            self.cache_db_class.delete(cache_id)
            return True
        
        return False

