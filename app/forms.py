from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, FloatField, DateField, DateTimeField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Email, NumberRange
from flask_wtf.file import FileAllowed
from .models import User
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
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    date = DateTimeField('Booking Date', format='%Y-%m-%d', validators=[DataRequired()])
    number_of_people = IntegerField('Number of People', validators=[DataRequired()])
    submit = SubmitField('Book Tour')


class TourForm(FlaskForm):
    name = StringField('Tour Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    available_spots = IntegerField('Available Spots', validators=[DataRequired()])
    images = FileField('Tour Images', validators=[FileAllowed(['jpg', 'png'], 'Images only!')], render_kw={"multiple": True})  # Поле для декількох зображень
    submit = SubmitField('Save Tour')






class DiscountForm(FlaskForm):
    discount_percentage = IntegerField('Discount Percentage', validators=[DataRequired(), NumberRange(min=0, max=100)])
    submit = SubmitField('Apply Discount')
