from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email
from app.models import User
from datetime import datetime
import re

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password should be at least 8 characters long.'),
        EqualTo('confirm_password', message='Passwords must match.')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_password(self, password):
        if not re.search(r'[A-Z]', password.data):
            raise ValidationError('Password must contain at least one uppercase letter.')
        if not re.search(r'[0-9]', password.data):
            raise ValidationError('Password must contain at least one digit.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is already registered. Please log in.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No account found with this username.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and user.password != password.data:
            raise ValidationError('Incorrect password.')

class BookingForm(FlaskForm):
    date = DateTimeField('Date', validators=[DataRequired()])
    number_of_people = IntegerField('Number of People', validators=[DataRequired()])
    submit = SubmitField('Book Now')
    def validate_number_of_people(self, number_of_people):
        if number_of_people.data <= 0:
            raise ValidationError('Number of people must be greater than 0.')

    def validate_date(self, date):
        if date.data < datetime.now():
            raise ValidationError('Booking date must be in the future.')

class TourForm(FlaskForm):
    name = StringField('Tour Name', validators=[DataRequired(), Length(max=80)])
    description = StringField('Description', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired()])
    date = DateTimeField('Date', validators=[DataRequired()])
    available_spots = IntegerField('Available Spots', validators=[DataRequired()])
    submit = SubmitField('Add Tour')

    def validate_price(self, price):
        if price.data <= 0:
            raise ValidationError('Price must be greater than 0.')

    def validate_date(self, date):
        if date.data < datetime.now():
            raise ValidationError('The tour date must be in the future.')

