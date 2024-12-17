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
    category = SelectField("Category", choices=["Mobile network connection", "PC network connection",\
         "PC hardware", "PC software", "Printer"],\
         validators=[DataRequired(), ])
    title = StringField("Title", validators=[DataRequired(), length(max=50)])
    ticket_details = TextAreaField("Details", validators=[DataRequired()])
    submit = SubmitField('Submit')

class NewUser(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired()])
    user_name = StringField("User Name", validators=[DataRequired(), length(min=2, max=20)])
    email = EmailField("E-mail", validators=[Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo('password')])

    #update the user type to be a string field based on the drop down list came from front end to be more simple and scalable
    user_type = StringField("User Type", validators=[DataRequired(), length(min=2, max=20)])
    # user_type = SelectField("User Type", choices=["Tech", "Non-Tech"], validate_choice=True)

    #update the user department to be a string field based on the drop down list came from front end to be more simple and scalable
    user_department = StringField("User Department", validators=[DataRequired(), length(min=2, max=20)])
    #user_department = SelectField("User Department", choices=["IT", "Accountant", "HR", "Operation", "Supply Chain", "Stock Control", "Admin", "Quality Control"])
    
    #update the user job to be a string field based on the drop down list came from front end to be more simple and scalable
    user_job = StringField("User User Job Title", validators=[DataRequired(), length(min=2, max=20)])
    # user_job = SelectField("User Job Title", choices=["IT", "Accountant", "HR", "Operation", "Logistics"])
    
    submit = SubmitField("Create")

class SearchTicket(FlaskForm):
    ticket_number = IntegerField("Ticket Number", validators=[DataRequired()])
    ticket_title = StringField("Ticket Title", validators=[DataRequired(), length(max=50)])
    submit = SubmitField("Find Ticket")

class SearchUser(FlaskForm):
    user_id = IntegerField("User ID", validators=[DataRequired()])
    username = StringField("User Name", validators=[DataRequired(), length(min=2, max=20)])
    submit = SubmitField("Find User")
