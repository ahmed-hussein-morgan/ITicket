# type: ignore
from flask import render_template, session, redirect, url_for, flash
from . import main
from .. import db, bcrypt
from .forms import LoginForm, NewTicketForm, NewUserForm, SearchTicketForm, SearchUserForm
from app.models import User, Ticket, IT, UserTicket

import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

@main.route("/login", methods=["GET", "POST"])
@main.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        if form.email.data == "admin@iticket.com" and form.password.data == "password":

            # session["email"] = request.form.get("email")

            session["email"] = form.email.data

            # flashed messaag below is using email data temporarly until we update the register form and database to get the 
            # username instead 
            flash(f"Welcome {form.email.data}!", 'success')

            # redireced below is to the home page temporarly until we update the database to redirect the user to his home
            # page based on the user type (tech/non-tech)
            return redirect(url_for('home'))

        else:
            flash("Login Unsuccessful. Please check username and password", "danger")

    return render_template("login.html", title="ITicket - Login", form=form)

@main.route("/home", methods=["GET", "POST"])
@main.route("/new-ticket", methods=["GET", "POST"])
def non_tech_new_ticket():
    return render_template("non-tech_add_ticket.html", title="ITicket - New Ticket")

@main.route("/all-tickets")
def all_ticket():
    return render_template("non-tech_all-tickets.html", title="ITicket - User Dashboard")

@main.route("/tech-dashboard")
def tech_dashboard():
    return render_template("tech_all-tickets.html", title="ITicket - User Dashboard")


@main.route("/new-tech-ticket", methods=["GET", "POST"])
def tech_new_ticket():
    return render_template("tech_add_ticket.html", title="ITicket - New Ticket")


@main.route("/update-ticket", methods=["GET", "POST"])
def update_ticket():
    return render_template("tech_update_ticket.html", title="ITicket - User Dashboard")

@main.route("/new-user", methods=["GET", "POST"])
def new_user():
    form = NewUserForm()
    if form.validate_on_submit():
        try:
            user_id = form.user_id.data
            user_name = form.user_name.data
            email = form.email.data
            user_type = form.user_type.data
            user_department = form.user_department.data
            user_job =form.user_job.data
            user_branch = form.user_branch.data
            user_status = form.user_status.data
            password = form.password.data



            # password = form.password.data
            user = User(id=user_id, employee_name=user_name, department=user_department, job_title=user_job, role_type=user_type, email=email, branch=user_branch, user_status=user_status)
            user.set_password(password)
            
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'User created successfully for {form.employee_name.data}.', 'success')


            # Debug logging

            #This modification will help you identify if the issue is with the route definition or if there's an exception being raised after the successful database commit.

            import logging
            logging.info(f"User created successfully. Redirecting to tech_dashboard.")



            return redirect(url_for('tech_dashboard'))
        except Exception as e:
            db.session.rollback()
            error_message = str(e)
            return render_template('register.html', form=form, error=error_message)
    return render_template('register.html', form=form)      


@main.route("/update-user", methods=["GET", "POST"])
def update_user():
    return render_template("tech_update_user.html", title="ITicket - User Dashboard")


@main.route("/delete-user", methods=["GET", "POST"])
def delete_user():
    return render_template("tech_delete_user.html", title="ITicket - User Dashboard")

@main.route("/all-users", methods=["GET", "POST"])
def all_users():
    return render_template("tech_all_users.html", title="ITicket - User Dashboard")
