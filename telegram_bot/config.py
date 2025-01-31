import os
import sys
from pathlib import Path

import django
from dotenv import load_dotenv


def django_setup():
    sys.path.append(f'{Path(__file__).resolve().parent.parent}/dj')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dj.settings")
    django.setup()


load_dotenv(dotenv_path=f'{Path(__file__).resolve().parent}/.env')

BOT_TOKEN = os.getenv('BOT_TOKEN')

BOT_WEBHOOK_URL = os.getenv('BOT_WEBHOOK_URL')
BOT_WEBHOOK_PATH = os.getenv('BOT_WEBHOOK_PATH')
BOT_SERVER_HOST = os.getenv('BOT_SERVER_HOST')
BOT_SERVER_PORT = int(os.getenv('BOT_SERVER_PORT'))

TELEGRAM_SECRET = os.getenv('TELEGRAM_SECRET')

CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
GROUP_ID = int(os.getenv('GROUP_ID'))

YOOKASSA_ID = os.getenv('YOOKASSA_ID')
YOOKASSA_SECRET = os.getenv('YOOKASSA_SECRET')
YOOKASSA_WEBHOOK_PATH = os.getenv('YOOKASSA_WEBHOOK_PATH')

django_setup()
