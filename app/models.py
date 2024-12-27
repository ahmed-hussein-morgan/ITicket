# type: ignore

# the statement above ^^ "# type: ignore" is necessary to ignore the Mypy type checker error

# This model is for creating the database and tables using AQLALCHEMY Database configuered in the config.py file

from sqlalchemy.sql.expression import func
from sqlalchemy import text, Index

from werkzeug.security import generate_password_hash, check_password_hash

# from flask_bcrypt import Bcrypt 
# from flask_sqlalchemy import SQLAlchemy

from app import db

# db = SQLAlchemy()
# bcrypt = Bcrypt()

# Ignore the Role table now from the database scheme for simplicity (recreate and update later )
#       Replace it by a string colomn in the Employee table to store the usert type for now (tech / non-tech)



# class Role(db.Model):
#     """ A table containes different types of roles """
#     __tablename__ = "roles"
#     id = db.Column(db.Integer, primary_key=True, unique=True)

#     # change the data type in the "role_type" column to be string
#     # instead of enum(drop-down list) to make it scalable if we need to add new role
#     # in the future. inthis case all we have to do is to add the new option to the drop-down list in the html page
#     # without need to update the enum lis of database too
     
#     # role_type = db.Column(db.Enum(RoleType), nullable=False)
#     role_type = db.Column(db.String(20), nullable=False)

#     def __repr__(self):
#         return f'<Role {self.role_type}>'

#     users = db.relationship("User", backref=db.backref("role", lazy=True))



# class User(db.Model):
#     """ A table containes employees data """
#     __tablename__ = "employees"
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     employee_name = db.Column(db.String(20), nullable=False, unique=True)
#     department = db.Column(db.String(20), nullable=False)
#     job_title = db.Column(db.String(20), nullable=False)
#     role_type_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
#     email = db.Column(db.String(64), nullable=False)
#     password = db.Column(db.String(256), nullable=False)
#     branch = db.Column(db.String(30), nullable=False)

#     # We have to handle the case of disabled user (Remove (ability to login (error message "This user has been removed or disabled. Contact your adminisatrator." (to enable or recreate it.) + Remove his database access and previlages)
#     # user_status = db.Column(db.Enum(UserStatus), nullable=False, default="Enabled")
#     user_status = db.Column(db.String(20), nullable=False, default="Enabled")


    # roles = db.relationship("Role", backref="user")

class User(db.Model):
    """ A table containing employees data """
    __tablename__ = "employees"


#     This argument is used to tell SQLAlchemy to extend an existing table instead of trying to create a new one. It's particularly useful when:

# You're working with an existing database schema that you don't want to recreate.
# You're making changes to your model definitions that don't match the existing database structure.
# You want to avoid conflicts when multiple parts of your application might be defining the same table.
# Relationship to database migrations:
# While __table_args__ = {'extend_existing': True} can help with some schema changes, it's not a replacement for proper database migrations. Here's why:

# It doesn't automatically update the database schema. It just tells SQLAlchemy to work with the existing table structure.
# It doesn't handle complex schema changes like adding or removing columns, changing column types, or modifying relationships between tables.
# It doesn't provide a way to track changes over time or roll back changes if needed.
# When to use __table_args__ = {'extend_existing': True}:
# During development when you're frequently changing your models and don't want to recreate the database each time.
# When working with an existing database that you can't easily recreate.
# As a temporary solution to avoid immediate conflicts while you're in the process of setting up proper migrations.
# Best practices:
# For production applications, it's generally better to use proper database migration tools like Flask-Migrate (which you're already using).
# Migrations provide a more robust way to manage schema changes over time, allowing you to track changes, roll back if needed, and apply changes to different environments (development, staging, production).
    __table_args__ = {'extend_existing': True}


    id = db.Column(db.Integer, primary_key=True, nullable=False)
    employee_name = db.Column(db.String(20), nullable=False, unique=True)
    department = db.Column(db.String(20), nullable=False)
    job_title = db.Column(db.String(20), nullable=False)

    role_type = db.Column(db.String(20), nullable=False)
    # role_type_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    email = db.Column(db.String(64), nullable=False)

    password_hash = db.Column(db.String(256), nullable=False)

    # @property
    # def password(self):
    #     raise AttributeError('password is not a readable attribute')
    
    # @password.setter
    # def password(self, password):
    #     self.hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # def verify_password(self, password):
    #     return bcrypt.check_password_hash(self.hashed_password, password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)



    branch = db.Column(db.String(30), nullable=False)
    user_status = db.Column(db.String(20), nullable=False, default="Enabled")

# class Ticket(db.Model):
#     """ A table that containes all the ticket details """
#     __tablename__ = "tickets"
#     ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

#     # select the ticket type (Request / Complain)
#     # ticket_type = db.Column(db.Enum(TicketType), nullable=False)
#     ticket_type = db.Column(db.String(20), nullable=False)

#     # ticket_category = db.Column(db.String(64), nullable=False) could be changed on productuon to be "enum" with limited category list
    
#     # Update the below line to show the Enum(Requests) wheb the Ticket type is "Request" or Enum(Complain) incase Ticket type is "Complain"
#     # Update it in the DB MySQL Server in addition to the below line using if
#     # Update the nullable=True to be False in both DB MySQL Server in addition to the below line

#     # if ticket_type == "REQUEST":
#     #     ticket_requests = db.Column(db.Enum(Requests), nullable=False)
#     # else:
#     #     ticket_requests = db.Column(db.Enum(Complains), nullable=False)

#     #ticket_category = db.Column(db.String(30), nullable=False)
#     ticket_title = db.Column(db.String(100), nullable=True)
#     ticket_details = db.Column(db.Text, nullable=True)

#     # Adding a column to add attached files like photos or screenshots (Canceled)because:
#     #       it needs an additional cost to store these files on a cloud 

#     # Pause for implementing the attachment now
#     # ticket_attachment = db.Column(db.)

#     submission_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
#     # submission_time = db.Column(db.Time, nullable=False, default=func.now().time())

#     # choose one from below methods to record the time by default 
#     # 1)
#     submission_time = db.Column(db.Time, nullable=False, default=text("TIME(CURRENT_TIMESTAMP)"))

#     # 2)
#     # submission_time = db.Column(db.Time, nullable=False, default=text("(CURRENT_TIMESTAMP TIME)"))

#     # 3)
#     # submission_time = db.Column(db.Time, nullable=False, default=func.now().cast(db.Time))


#     # ticket_status = db.Column(db.Enum(TicketStatus), nullable=False, default="Submitted")
#     ticket_status = db.Column(db.String(20), nullable=False, default="Submitted")

#     # tickets = db.relationship("IT", backref="ticket")
#     tickets = db.relationship("IT", backref=db.backref("ticket", lazy=True))

#     __table_args__ = (Index('ix_ticket_id', ticket_id),)

class Ticket(db.Model):
    """ A table that contains all the ticket details """
    __tablename__ = "tickets"

    __table_args__ = {'extend_existing': True}

    ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    ticket_type = db.Column(db.String(20), nullable=False)
    ticket_title = db.Column(db.String(100), nullable=True)
    ticket_details = db.Column(db.Text, nullable=True)
    submission_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
    submission_time = db.Column(db.Time, nullable=False, default=text("TIME(CURRENT_TIMESTAMP)"))
    ticket_status = db.Column(db.String(20), nullable=False, default="Submitted")
    tickets = db.relationship("IT", backref=db.backref("ticket", lazy=True))

# class IT(db.Model):
#     """ A table that containes some ticket details for tech users only """
#     __tablename__ = "it_tickets"
#     index = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
#     tech_name = db.Column(db.String(30), nullable=True)
#     update_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
#     # update_time = db.Column(db.Time, nullable=False, default=func.now().time())
#     update_ticket_comment = db.Column(db.Text, nullable=True)

class IT(db.Model):
    """ A table that contains some ticket details for tech users only """
    __tablename__ = "it_tickets"

    __table_args__ = {'extend_existing': True}

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
    tech_name = db.Column(db.String(30), nullable=True)
    update_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
    update_ticket_comment = db.Column(db.Text, nullable=True)

class UserTicket(db.Model):
    """ A linking table to link between the employee table and the ticket table """
    __tablename__ = "employee_ticket"

    __table_args__ = {'extend_existing': True}

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
    ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
