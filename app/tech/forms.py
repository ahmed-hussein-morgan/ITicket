# type: ignore
from flask import current_app
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, length, Email, EqualTo, DataRequired, ValidationError
from ..models import User, Ticket, IT, UserTicket


class NewUserForm(FlaskForm):
    # user_id = StringField("User ID", validators=[InputRequired()])
    user_id = IntegerField("User ID", validators=[InputRequired()])
    user_name = StringField("User Name", validators=[InputRequired(), length(min=2, max=20)])
    email = EmailField("E-mail", validators=[Email(), InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[InputRequired(), EqualTo('password', message='Passwords must match')])

    # confirm_password = PasswordField("Confirm Password", [validators.InputRequired(), validators.EqualTo(password)])

    #update the user type to be a string field based on the drop down list came from front end to be more simple and scalable
    # user_type = StringField("User Type", validators=[InputRequired(), length(min=2, max=20)])



    # coerce=int is parameter in WTForms is used with SelectField to ensure that the selected value is converted to an integer before being passed to the backend.
    #      It tells WTForms to convert the selected value to an integer before passing it to your form handler.
    #           By default, SelectField expects the values of its choices to be integers, but often you want to display human-readable strings (like "Tech" or "Non-Tech") while storing numeric IDs in the database.
    #           With coerce=int, you can provide string labels in your choices, but WTForms will automatically convert the selected value to an integer before sending it to your backend. 
    # For example:
    # choices=[(1, "Tech"), (2, "Non-Tech")]
    # user_type = SelectField("User Type", coerce=int, choices=[(role.id, role.role_type) for role in Role.query.all()], validators=[InputRequired()])
    
    # 1- We move the population of user_type.choices to the __init__ method of the form.
    # This ensures that the database query only happens when the form is instantiated,
    # which will always be within an application context.
    # 2- We remove the dynamic choice generation from the field definition,
    # replacing it with a simple InputRequired() validator


    
    # user_type = SelectField("User Type", coerce=int, validators=[InputRequired()])

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    #     with current_app.app_context():
    #         self.user_type.choices = [(role.id, role.role_type) for role in Role.query.all()]
    
    user_type = SelectField("User Type", choices=["", "Tech", "Non-Tech"], validate_choice=True, validators=[InputRequired()] )

    #update the user department to be a string field based on the drop down list came from front end to be more simple and scalable
    user_department = SelectField("User Department", choices=["", "Accountant", "Operation", "HR", "IT", "Admin", "Stock Control", "Supply Chain", "Quality Control"], validators=[InputRequired()], validate_choice=True)
    #user_department = SelectField("User Department", choices=["IT", "Accountant", "HR", "Operation", "Supply Chain", "Stock Control", "Admin", "Quality Control"])
    
    #update the user job to be a string field based on the drop down list came from front end to be more simple and scalable
    # user_job = StringField("User Job Title", validators=[InputRequired(), length(min=2, max=20)])
    user_job = SelectField("User Job Title", choices=["", "Web Developer", "Accountant", "HR Generalist", "Team Leader", "Section head"], validate_choice=True, validators=[InputRequired()] )


    user_branch = SelectField("User Branch", choices=["", "Head Quarter", "Heliopolis", "Nasr City", "New Cairo", "6th October"], validate_choice=True, validators=[InputRequired()] )
    # user_branch = StringField("User Branch", validators=[InputRequired(), length(min=2, max=20)])


    user_status = SelectField("User Status", choices=["", "Enabled", "Disabled"], validate_choice=True, validators=[InputRequired()], default="Enabled" )
    # user_status = StringField("User Status", validators=[InputRequired(), length(min=2, max=20)])
    
    submit = SubmitField("Create")


    def validate_user_id(self, user_id):
        id = User.query.filter_by(id=user_id.data).first()
        
        if user_id.data < 1:
            raise ValidationError("User ID can not be less than 1")

        elif id:
            raise ValidationError("This User ID is already exist. Please choose another one")
        

        

    def validate_user_name(self, user_name):
        name = User.query.filter_by(employee_name=user_name.data).first()

        if name:
            raise ValidationError("This User Name is already exist. Please choose another one")

        
    def validate_email(self, email):
        user_email = User.query.filter_by(email=email.data).first()

        if user_email:
            raise ValidationError("This Email is already exist. Please choose another one")



class SearchTicketForm(FlaskForm):
    ticket_number = IntegerField("Ticket Number", validators=[InputRequired()])
    ticket_title = StringField("Ticket Title", validators=[InputRequired(), length(max=50)])
    submit = SubmitField("Find Ticket")

class SearchUserForm(FlaskForm):
    user_id = IntegerField("User ID", validators=[InputRequired()])
    username = StringField("User Name", validators=[InputRequired(), length(min=2, max=20)])
    submit = SubmitField("Find User")
