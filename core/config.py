import hashlib
import os
from icecream import ic
from decouple import Config, RepositoryEnv, Csv

# .env file path
ENV_FILE = 'core/data/.env'

# Check if .env exists
if not os.path.exists(ENV_FILE):
    ic('.env fayli topilmadi!')
    ic('.env.example faylidan nusxa ko\'chirib shablonni o\'zizga moslang.')
    exit(1)

# Load .env
env = Config(repository=RepositoryEnv(ENV_FILE))

# Read values
BOT_TOKEN = env('BOT_TOKEN')
ADMINS = env('ADMINS', cast=Csv())
WEBHOOK_DOMAIN = env('WEBHOOK_DOMAIN')
SECRET_KEY = env('SECRET_KEY')
BASE_URL = env('BASE_URL')
DEBUG = env('DEBUG', cast=bool)
ALLOWED_HOSTS = env('ALLOWED_HOSTS', cast=Csv())
CSRF_TRUSTED_ORIGINS = env('CSRF_TRUSTED_ORIGINS', cast=Csv())

# Create webhook path & url
WEBHOOK_PATH = hashlib.md5(BOT_TOKEN.encode()).hexdigest()
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}/api/webhook/{WEBHOOK_PATH}"

BEARER_AUTH_TOKEN = env('BEARER_AUTH_TOKEN')
