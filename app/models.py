from flask_login import UserMixin
from .config import db
from datetime import datetime

# Модель користувача
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)

    def check_password(self, password):
        return self.password == password

# Модель туру
class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    available_spots = db.Column(db.Integer, nullable=False, default=10)

    def __repr__(self):
        return f'<Tour {self.name}>'

    def is_available(self, spots_needed):
        return self.available_spots >= spots_needed

# Модель бронювання
class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)
    number_of_people = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    total_price = db.Column(db.Float, nullable=False)

    user = db.relationship('User', backref='bookings')
    tour = db.relationship('Tour', backref='bookings')
    def __repr__(self):
        return f'<Booking {self.id} for Tour {self.tour_id}>'
