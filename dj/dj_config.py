import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=f'{Path(__file__).resolve().parent}/.env')

DJANGO_SECRET = os.getenv('DJANGO_SECRET')
BOT_TOKEN = os.getenv('BOT_TOKEN')

DEBUG = bool(int(os.getenv('DEBUG')))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(',')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(',')
CORS_ALLOW_ALL_ORIGINS = bool(int(os.getenv('CORS_ALLOW_ALL_ORIGINS')))
CORS_ALLOW_CREDENTIALS = bool(int(os.getenv('CORS_ALLOW_CREDENTIALS')))

DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')