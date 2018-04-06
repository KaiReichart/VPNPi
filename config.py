import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Kaireichart1997'
    FLASK_DEBUG = 1
