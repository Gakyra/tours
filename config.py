import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MIGRATION_DIR = os.path.join(basedir, 'migrations')
    DEBUG = False
    CACHE_TYPE = 'SimpleCache'
    CACHE_DEFAULT_TIMEOUT = 300
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)

def get_config(env='development'):
    config_classes = {
        'development': Config,
        'production': Config
    }
    return config_classes.get(env, Config)
