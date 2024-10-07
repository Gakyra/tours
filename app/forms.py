from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FloatField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, NumberRange


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BookingForm(FlaskForm):
    tour_id = IntegerField('Tour ID', validators=[DataRequired()])
    number_of_people = IntegerField('Number of People', validators=[DataRequired(), NumberRange(min=1)])
    date = DateTimeField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Book Now')

class TourForm(FlaskForm):
    name = StringField('Tour Name', validators=[DataRequired(), Length(min=3, max=80)])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    date = DateTimeField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save')
