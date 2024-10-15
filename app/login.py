from .config import app, login_manager
from .models import User


__all__ = ('load_user',)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))