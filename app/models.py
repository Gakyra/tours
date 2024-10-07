from flask_sqlalchemy import SQLAlchemy  # Імпорт SQLAlchemy для роботи з базою даних
from flask_login import UserMixin  # Імпорт UserMixin для управління аутентифікацією

db = SQLAlchemy()  # Ініціалізація SQLAlchemy

# Модель користувача
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор користувача
    username = db.Column(db.String(64), unique=True, nullable=False)  # Ім'я користувача
    password = db.Column(db.String(128), nullable=False)  # Пароль користувача

# Модель туру
class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор туру
    name = db.Column(db.String(80), nullable=False)  # Назва туру
    description = db.Column(db.Text, nullable=False)  # Опис туру
    price = db.Column(db.Float, nullable=False)  # Ціна туру
    date = db.Column(db.DateTime, nullable=False)  # Дата туру
    available_spots = db.Column(db.Integer, nullable=False)  # Кількість доступних місць

# Модель бронювання
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор бронювання
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  # Ідентифікатор користувача, який зробив бронювання
    tour_id = db.Column(db.Integer, db.ForeignKey('tour.id'), nullable=False)  # Ідентифікатор туру
    number_of_people = db.Column(db.Integer, nullable=False)  # Кількість людей для бронювання
    date = db.Column(db.DateTime, nullable=False)  # Дата бронювання
    total_price = db.Column(db.Float, nullable=False)  # Загальна ціна за бронювання
