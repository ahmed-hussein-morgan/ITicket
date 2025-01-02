# type: ignore
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.sql.expression import func
from sqlalchemy import text, Index
from config import get_config
import logging
from flask_login import LoginManager

# from flask_bcrypt import Bcrypt
# from flask_wtf.csrf import CSRFProtect



bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


# The login_view attribute of the LoginManager object sets the endpoint for the login page.

login_manager.login_view = 'auth.login'
# bcrypt = Bcrypt()
# csrf = CSRFProtect()

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

# class User(db.Model):
#     """ A table containing employees data """
#     __tablename__ = "employees"
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     employee_name = db.Column(db.String(20), nullable=False, unique=True)
#     department = db.Column(db.String(20), nullable=False)
#     job_title = db.Column(db.String(20), nullable=False)

#     role_type = db.Column(db.String(20), nullable=False)
#     # role_type_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    
#     email = db.Column(db.String(64), nullable=False)

#     password_hash = db.Column(db.String(256), nullable=False)

#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
    
#     @password.setter
#     def password(self, password):
#         self.hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

#     def verify_password(self, password):
#         return bcrypt.check_password_hash(self.hashed_password, password)



#     branch = db.Column(db.String(30), nullable=False)
#     user_status = db.Column(db.String(20), nullable=False, default="Enabled")

# # class Ticket(db.Model):
# #     """ A table that containes all the ticket details """
# #     __tablename__ = "tickets"
# #     ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)

# #     # select the ticket type (Request / Complain)
# #     # ticket_type = db.Column(db.Enum(TicketType), nullable=False)
# #     ticket_type = db.Column(db.String(20), nullable=False)

# #     # ticket_category = db.Column(db.String(64), nullable=False) could be changed on productuon to be "enum" with limited category list
    
# #     # Update the below line to show the Enum(Requests) wheb the Ticket type is "Request" or Enum(Complain) incase Ticket type is "Complain"
# #     # Update it in the DB MySQL Server in addition to the below line using if
# #     # Update the nullable=True to be False in both DB MySQL Server in addition to the below line

# #     # if ticket_type == "REQUEST":
# #     #     ticket_requests = db.Column(db.Enum(Requests), nullable=False)
# #     # else:
# #     #     ticket_requests = db.Column(db.Enum(Complains), nullable=False)

# #     #ticket_category = db.Column(db.String(30), nullable=False)
# #     ticket_title = db.Column(db.String(100), nullable=True)
# #     ticket_details = db.Column(db.Text, nullable=True)

# #     # Adding a column to add attached files like photos or screenshots (Canceled)because:
# #     #       it needs an additional cost to store these files on a cloud 

# #     # Pause for implementing the attachment now
# #     # ticket_attachment = db.Column(db.)

# #     submission_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
# #     # submission_time = db.Column(db.Time, nullable=False, default=func.now().time())

# #     # choose one from below methods to record the time by default 
# #     # 1)
# #     submission_time = db.Column(db.Time, nullable=False, default=text("TIME(CURRENT_TIMESTAMP)"))

# #     # 2)
# #     # submission_time = db.Column(db.Time, nullable=False, default=text("(CURRENT_TIMESTAMP TIME)"))

# #     # 3)
# #     # submission_time = db.Column(db.Time, nullable=False, default=func.now().cast(db.Time))


# #     # ticket_status = db.Column(db.Enum(TicketStatus), nullable=False, default="Submitted")
# #     ticket_status = db.Column(db.String(20), nullable=False, default="Submitted")

# #     # tickets = db.relationship("IT", backref="ticket")
# #     tickets = db.relationship("IT", backref=db.backref("ticket", lazy=True))

# #     __table_args__ = (Index('ix_ticket_id', ticket_id),)

# class Ticket(db.Model):
#     """ A table that contains all the ticket details """
#     __tablename__ = "tickets"
#     ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
#     ticket_type = db.Column(db.String(20), nullable=False)
#     ticket_title = db.Column(db.String(100), nullable=True)
#     ticket_details = db.Column(db.Text, nullable=True)
#     submission_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
#     submission_time = db.Column(db.Time, nullable=False, default=text("TIME(CURRENT_TIMESTAMP)"))
#     ticket_status = db.Column(db.String(20), nullable=False, default="Submitted")
#     tickets = db.relationship("IT", backref=db.backref("ticket", lazy=True))

# # class IT(db.Model):
# #     """ A table that containes some ticket details for tech users only """
# #     __tablename__ = "it_tickets"
# #     index = db.Column(db.Integer, primary_key=True, autoincrement=True)
# #     ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
# #     tech_name = db.Column(db.String(30), nullable=True)
# #     update_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
# #     # update_time = db.Column(db.Time, nullable=False, default=func.now().time())
# #     update_ticket_comment = db.Column(db.Text, nullable=True)

# class IT(db.Model):
#     """ A table that contains some ticket details for tech users only """
#     __tablename__ = "it_tickets"
#     index = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
#     tech_name = db.Column(db.String(30), nullable=True)
#     update_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
#     update_ticket_comment = db.Column(db.Text, nullable=True)

# class UserTicket(db.Model):
#     """ A linking table to link between the employee table and the ticket table """
#     __tablename__ = "employee_ticket"
#     index = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
#     ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)

# class Role(db.Model):
#     """ A table containing different types of roles """
#     __tablename__ = "roles"
#     id = db.Column(db.Integer, primary_key=True, unique=True)
#     role_type = db.Column(db.String(20), nullable=False)
#     users = db.relationship("User", backref=db.backref("role", lazy=True))

# class User(db.Model):
#     """ A table containing employees data """
#     __tablename__ = "employees"
#     id = db.Column(db.Integer, primary_key=True, nullable=False)
#     employee_name = db.Column(db.String(20), nullable=False, unique=True)
#     department = db.Column(db.String(20), nullable=False)
#     job_title = db.Column(db.String(20), nullable=False)
#     role_type_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
#     email = db.Column(db.String(64), nullable=False)

#     password_hash = db.Column(db.String(256), nullable=False)

#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
    
#     @password.setter
#     def password(self, password):
#         self.hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

#     def verify_password(self, password):
#         return bcrypt.check_password_hash(self.hashed_password, password)



#     branch = db.Column(db.String(30), nullable=False)
#     user_status = db.Column(db.String(20), nullable=False, default="Enabled")

# class Ticket(db.Model):
#     """ A table that contains all the ticket details """
#     __tablename__ = "tickets"
#     ticket_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
#     ticket_type = db.Column(db.String(20), nullable=False)
#     ticket_title = db.Column(db.String(100), nullable=True)
#     ticket_details = db.Column(db.Text, nullable=True)
#     submission_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
#     submission_time = db.Column(db.Time, nullable=False, default=text("TIME(CURRENT_TIMESTAMP)"))
#     ticket_status = db.Column(db.String(20), nullable=False, default="Submitted")
#     tickets = db.relationship("IT", backref=db.backref("ticket", lazy=True))

# class IT(db.Model):
#     """ A table that contains some ticket details for tech users only """
#     __tablename__ = "it_tickets"
#     index = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)
#     tech_name = db.Column(db.String(30), nullable=True)
#     update_date = db.Column(db.Date, nullable=False, default=func.now().cast(db.Date))
#     update_ticket_comment = db.Column(db.Text, nullable=True)

# class UserTicket(db.Model):
#     """ A linking table to link between the employee table and the ticket table """
#     __tablename__ = "employee_ticket"
#     index = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=False)
#     ticket_id = db.Column(db.Integer, db.ForeignKey('tickets.ticket_id'), nullable=False)

def Create_app(config_name='development'):

    app = Flask(__name__)
    config_class = get_config(config_name)
    config_class.init_app(app)
    # bcrypt = Bcrypt(app)

    # Set up logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    # bcrypt.init_app(app)
    # csrf.init_app(app)


    from .main import main as main_blueprint  # Import blueprint
    app.register_blueprint(main_blueprint)


    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)



        # Create tables within the app context
    with app.app_context():
        print("Creating tables...")
        db.create_all()  # This will create tables for all defined models
        print("All tables created successfully.")


    return app
