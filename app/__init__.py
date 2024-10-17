# The imports sequence MUST be the following
from .login import *
from .routes import *
from .config import app, db
from .create_admin import create_admin


with app.app_context():
    create_admin()
