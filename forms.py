from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class UserSignupForm(FlaskForm):
    first_name = StringField('First Name: ', validators = [DataRequired()])
    last_name = StringField('Last Name: ', validators = [DataRequired()])
    email = StringField('Email: ', validators = [DataRequired(), Email()])
    username = StringField('Username: ', validators = [DataRequired()])
    password = PasswordField('Password: ', validators = [DataRequired()])
    submit_button = SubmitField()

class UserLoginForm(FlaskForm):
    username = StringField('Username: ', validators = [DataRequired()])
    password = PasswordField('Password: ', validators = [DataRequired()])
    submit_button = SubmitField()

class CarCreationForm(FlaskForm):
    make = StringField('Make: ', validators = [DataRequired()])
    model = StringField('Model: ', validators = [DataRequired()])
    year = StringField('Year: ', validators = [DataRequired()])
    user_token = StringField('Your Token: ', validators = [DataRequired()])
    submit_button = SubmitField()


