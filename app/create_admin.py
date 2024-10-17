from app.models import User
from app import db

def create_admin():
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', email='admin@example.com', is_admin=True)
        admin.set_password('adminpassword')
        db.session.add(admin)
        db.session.commit()
        print("Адміністратор створений.")
    else:
        print("Адміністратор вже існує.")
