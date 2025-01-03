# type: ignore
from flask import current_app
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, SelectField, TextAreaField, IntegerField
from wtforms.validators import InputRequired, length, Email, EqualTo, DataRequired, ValidationError
from ..models import User, Ticket, IT, UserTicket



class NewTicketForm(FlaskForm):
    # ticket_number = Ticket.query.filter_by(ticket_id).last()
    # if ticket_number is None or ticket_number == 0:
    #     ticket_number = 1
    # else:
    #     ticket_number += 1

    # id = IntegerField("Ticket ID", validators=[InputRequired, length(1, 6)], default=ticket_number, render_kw={'readonly': True})

    
    ticket_branch = SelectField("Ticket Branch", choices=["", "Head Quarter", "Heliopolis", "Nasr City", "New Cairo", "6th October"], validate_choice=True, validators=[InputRequired()])   
  
    ticket_type = SelectField("Ticket Type", choices=["","Request", "Complain"], validators=[InputRequired()],  validate_choice=True)    
    category = SelectField("Category", choices=["", "Mobile network connection", "PC network connection",\
         "PC hardware", "PC software", "Printer", "Mouse", "Keboard"],\
         validators=[InputRequired()],  validate_choice=True)
    title = StringField("Title", validators=[InputRequired(), length(max=50)])
    ticket_details = TextAreaField("Details", validators=[InputRequired()])
    submit = SubmitField('Submit')



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.generate_ticket_number()

    def generate_ticket_number(self):
        with current_app.app_context():
            latest_ticket = Ticket.query.order_by(Ticket.ticket_id.desc()).first()
            if latest_ticket:
                self.ticket_number = latest_ticket.ticket_id + 1
            else:
                self.ticket_number = 1

    @property
    def ticket_number(self):
        return IntegerField("Ticket ID", validators=[InputRequired, length(1, 6)], render_kw={'readonly': True})    

    def validate_ticket_type(self, ticket_type):
        if ticket_type == "":
            raise ValidationError("Ticket Type can't be empty. You have to choose a type.")
        
    def validate_ticket_branch(self, ticket_branch):
        if ticket_branch == "":
            raise ValidationError("Ticket Branch can't be empty. You have to choose the branch.")
        

    def validate_ticket_category(self, category):
        if category == "":
            raise ValidationError("Ticket Title can't be empty.")
