import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///sentinel.db')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    ELASTICSEARCH_URL = os.getenv('ELASTICSEARCH_URL', 'http://localhost:9200')
    HONEYPOT_PORT = int(os.getenv('HONEYPOT_PORT', 2222))
    API_PORT = int(os.getenv('API_PORT', 8000))
    DEBUG = True

config = Config()
