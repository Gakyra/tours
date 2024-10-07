from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_caching import Cache
from datetime import timedelta

__all__ = ('app', 'db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
cache = Cache(app)

from app.models import User
from app.routes import *

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
