import hashlib
import os
from icecream import ic
from decouple import Config, RepositoryEnv, Csv

# Paths
ENV_FILE = 'core/data/.env'
SERVICE_ACCOUNT_FILE = 'core/data/service-account.json'

# Check if .env exists
if not os.path.exists(ENV_FILE):
    ic('.env fayli topilmadi!')
    ic('.env.example faylidan nusxa ko\'chirib shablonni o\'zizga moslang.')
    exit(1)

# Check if service-account.json exists
if not os.path.exists(SERVICE_ACCOUNT_FILE):
    ic('service-account.json fayli topilmadi!')
    ic('Iltimos, Firebase uchun kerakli JSON faylni quyidagi joyga qo\'шing:')
    ic(SERVICE_ACCOUNT_FILE)
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
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', cast=bool, default=True)

# Create webhook path & url
WEBHOOK_PATH = hashlib.md5(BOT_TOKEN.encode()).hexdigest()
WEBHOOK_URL = f"{WEBHOOK_DOMAIN}/api/webhook/{WEBHOOK_PATH}"

BEARER_AUTH_TOKEN = env('BEARER_AUTH_TOKEN')
