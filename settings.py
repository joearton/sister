import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

BASE_DIR     = os.path.dirname(__file__)
CACHE_DIR    = os.path.join(BASE_DIR, '.cache')
CONFIG_DIR   = os.path.join(BASE_DIR, 'config')
API_KEY_FILE = os.path.join(CACHE_DIR, 'api_key.json')


if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)


# Environment variable configuration
def get_env_config():
    """Get configuration from environment variables"""
    config = {
        'sister_url': os.getenv('SISTER_URL'),
        'use_sandbox': os.getenv('USE_SANDBOX', 'true').lower() == 'true',
        'username': os.getenv('SISTER_USERNAME'),
        'password': os.getenv('SISTER_PASSWORD'),
        'id_pengguna': os.getenv('SISTER_ID_PENGGUNA'),
        'cache_expiration_days': int(os.getenv('CACHE_EXPIRATION_DAYS', '1')),
        'auto_cleanup_cache': os.getenv('AUTO_CLEANUP_CACHE', 'false').lower() == 'true',
        'api_timeout_seconds': int(os.getenv('API_TIMEOUT_SECONDS', '30')),
        'max_retries': int(os.getenv('MAX_RETRIES', '3'))
    }
    
    # Validate required environment variables
    required_vars = ['sister_url', 'username', 'password', 'id_pengguna']
    missing_vars = [var for var in required_vars if not config[var]]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        print("Please create a .env file with the required variables.")
        print("You can copy env.example to .env and fill in your credentials.")
        os.abort()
    
    return config


# Load configuration
ENV_CONFIG = get_env_config()


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

