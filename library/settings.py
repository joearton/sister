import os

BASE_DIR     = os.getcwd()
CACHE_DIR    = os.path.join(BASE_DIR, '.cache')
CONFIG_DIR   = os.path.join(BASE_DIR, 'config')
CONFIG_FILE  = os.path.join(CONFIG_DIR, 'config.json')
API_KEY_FILE = os.path.join(CACHE_DIR, 'api_key.json')


if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


if not os.path.isfile(CONFIG_FILE):
    print('Config file available, create it in '. CONFIG_FILE)
    os.abort()


STATUS_SUCCESS_WITH_REPLY   = 200
STATUS_SUCCESS              = STATUS_SUCCESS_WITH_REPLY
STATUS_SUCCESS_NO_REPLY     = 204
STATUS_REQ_INVALID          = 400
STATUS_TOKEN_INVALID        = 401
STATUS_CHANGES_DENIED       = 403
STATUS_ENDPOINT_NOTFOUND    = 404
STATUS_HTTP_DENIED          = 405
STATUS_ENDPOINT_EXIST       = 409
STATUS_ERROR                = 500


HTTP_METHOD_GET     = 'get'
HTTP_METHOD_POST    = 'post'
HTTP_METHOD_PATCH   = 'patch'
HTTP_METHOD_DELETE  = 'delete'

