# type: ignore
from flask import render_template, redirect, request, url_for, flash
from . import tech
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import NewUserForm, SearchTicketForm, SearchUserForm
from .. import db

@tech.route("/tech-dashboard")
def tech_dashboard():
    return render_template("tech_all-tickets.html", title="ITicket - User Dashboard")


@tech.route("/new-tech-ticket", methods=["GET", "POST"])
def tech_new_ticket():
    return render_template("tech_add_ticket.html", title="ITicket - New Ticket")


@tech.route("/update-ticket", methods=["GET", "POST"])
def update_ticket():
    return render_template("tech_update_ticket.html", title="ITicket - User Dashboard")

@tech.route("/new-user", methods=["GET", "POST"])
# @login_required
def new_user():

    # Check if the current user has permission to create new users
    # if not current_user.is_authenticated or not current_user.has_permission_to_create_users():
    #     flash("You don't have permission to create new users.", "warning")
    #     return redirect(url_for('auth.login'))


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
            
            flash(f'User created successfully for {form.user_name.data}.', 'success')


            # Debug logging

            #This modification will help you identify if the issue is with the route definition or if there's an exception being raised after the successful database commit.

            # import logging
            # logging.info(f"User created successfully. Redirecting to tech_dashboard.")



            return redirect(url_for('tech.all_users'))
        except Exception as e:
            db.session.rollback()
            error_message = str(e)
            return render_template('register.html', form=form, error=error_message)
    return render_template('tech_add_user.html', form=form, title="ITicket - New User")      


@tech.route("/update-user", methods=["GET", "POST"])
def update_user():
    return render_template("tech_update_user.html", title="ITicket - User Dashboard")


@tech.route("/delete-user", methods=["GET", "POST"])
def delete_user():
    return render_template("tech_delete_user.html", title="ITicket - User Dashboard")

@tech.route("/all-users", methods=["GET", "POST"])
def all_users():
    return render_template("tech_all_users.html", title="ITicket - User Dashboard")
