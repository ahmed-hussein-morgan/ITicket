# type: ignore

# the statement above ^^ "# type: ignore" is necessary to ignore the Mypy type checker error

# This model is for creating the database and tables using AQLALCHEMY Database configuered in the config.py file

from sqlalchemy.sql.expression import func
from sqlalchemy import text, Index
from enum import Enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# This model is for creating the database and tables
class RoleType(Enum):
    """ A drop-down list of different types of users """
    TECH = "tech"
    NON_TECH = "non-tech"

class TicketStatus(Enum):
    """ A drop-down list of different status of the ticket """
    OPEN = "open"
    RECEIVED = "received"
    SOLVED = "solved"

class TicketType(Enum):
    """ A drop-down list of different types of the ticket """
    REQUEST = "request"
    COMPLAIN = "complain"


class Requests(Enum):
    """ A drop-down list of different types of requests if the Ticket Type was Request """
    MOUSE = "new_mouse"
    KEYBOARD = "new_keyboard"
    CHARGER = "new_charger"
    CARTIDGE = "new_or_refill_cartidge"
    PC = "new_pc"
    OTHER = "other"

class Complains(Enum):
    """ A drop-down list of different types of complains if the Ticket Type was Complain """
    MOBILE_NETWORK = "mobile network connection"
    PC_NETWORK = "pc network connection"
    PC_HARDWARE = "pc hardware"
    PC_SOFTWARE = "pc software"
    PRINTER = "printer"
    OTHER = "other"



class Role(db.Model):
    """ A table containes different types of roles """
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True, unique=True)
    role_type = db.Column(db.Enum(RoleType), nullable=False)
    # users = db.relationship("User", backref="role", lazy=True)
    users = db.relationship("User", backref=db.backref("role", lazy=True))


class User(db.Model):
    """ A table containes employees data """
    __tablename__ = "employees"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    employee_name = db.Column(db.String(20), nullable=False, unique=True)
    department = db.Column(db.String(20), nullable=False)
    job_title = db.Column(db.String(20), nullable=False)
    role_type_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(256), nullable=False)
    branch = db.Column(db.String(30), nullable=False)
    # roles = db.relationship("Role", backref="user")

class Ticket(db.Model):
    """ A table that containes all the ticket details """
    __tablename__ = "tickets"
    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    ticket_type = db.Column(db.Enum(TicketType), nullable=False)
    # ticket_category = db.Column(db.String(64), nullable=False) could be changed on productuon to be "enum" with limited category list
    ticket_requests = db.Column(db.Enum(Requests), nullable=True)
    #ticket_category = db.Column(db.String(30), nullable=False)
    ticket_title = db.Column(db.String(64), nullable=True)
    ticket_details = db.Column(db.Text, nullable=True)

    # Adding a column to add attached files like photos or screenshots (Canceled)because:
    #       it either need an additional cost to store these files on a cloud 

    # Pause for implementing the attachment now
    # ticket_attachment = db.Column(db.)

    submission_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
    # submission_time = db.Column(db.Time, nullable=False, default=func.now().time())

    # choose one from below methods to record the time by default 
    # 1)
    submission_time = db.Column(db.Time, nullable=False, default=text("TIME(CURRENT_TIMESTAMP)"))

    # 2)
    # submission_time = db.Column(db.Time, nullable=False, default=text("(CURRENT_TIMESTAMP TIME)"))

    # 3)
    # submission_time = db.Column(db.Time, nullable=False, default=func.now().cast(db.Time))


    ticket_status = db.Column(db.Enum(TicketStatus), nullable=False)
    # tickets = db.relationship("IT", backref="ticket")
    tickets = db.relationship("IT", backref=db.backref("ticket", lazy=True))

    __table_args__ = (Index('ix_ticket_id', ticket_id),)



class IT(db.Model):
    """ A table that containes some ticket details for tech users only """
    __tablename__ = "it_tickets"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    tech_name = db.Column(db.String(30), nullable=True)
    update_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
    # update_time = db.Column(db.Time, nullable=False, default=func.now().time())
    update_ticket_details = db.Column(db.Text, nullable=True)

class UserTicket(db.Model):
    """ A linking table to link between the employee table and the ticket table """
    __tablename__ = "employee_ticket"
    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    
