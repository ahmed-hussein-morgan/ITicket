# type: ignore
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField 
from wtforms.validators import DataRequired, length, Email, EqualTo

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Username', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

