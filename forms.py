# type: ignore
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, length, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class NewTicket(FlaskForm):
    category = SelectField("Category", choices=["Mobile network connection", "PC networkconnection",\
         "PC hardware", "PC software", "Printer"],\
         validators=[DataRequired(), ])
    title = StringField("Title", validators=[DataRequired(), length(max=50)])
    ticket_details = TextAreaField("Details", validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewUser(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired()])
    username = StringField("User Name", validators=[DataRequired(), length(min=2, max=20)])
    email = EmailField("E-mail", validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])
    user_type = SelectField("Category", choices=["tech", "non-tech"], validate_choice=True)
    user_department = SelectField("Category", choices=["IT", "Accountant", "HR", "Operation", "Logistics"])
    submit = SubmitField("Create")

class SearchTicket(FlaskForm):
    ticket_number = IntegerField("Ticket Number", validators=[DataRequired()])
    ticket_title = StringField("Ticket Title", validators=[DataRequired(), length(max=50)])
    submit = SubmitField("Find Ticket")

class SearchUser(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired()])
    username = StringField("User Name", validators=[DataRequired(), length(min=2, max=20)])
    submit = SubmitField("Find User")
