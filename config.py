# config.py
import os
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    DEBUG = True

    DATABASE = os.path.join(BASE_DIR, 'siteprogsound.db')

    SECRET_KEY = os.getenv('SECRET_KEY', 'default')
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SAMESITE = 'Lax'
    REMEMBER_COOKIE_DURATION = timedelta(days=30)

    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    GOOGLE_DISCOVERY_URL = os.getenv('GOOGLE_DISCOVERY_URL')