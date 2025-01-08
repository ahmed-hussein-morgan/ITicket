# type: ignore
from flask import render_template, redirect, request, url_for, flash, current_app
from . import tech
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Ticket, IT, UserTicket
from .forms import NewUserForm, SearchTicketForm, SearchUserForm, NewTicketForm, UpdateUserForm
from .. import db
from datetime import datetime, timezone
from sqlalchemy import or_

@tech.route("/tech-dashboard")
def tech_dashboard():
    return render_template("tech_all-tickets.html", title="ITicket - User Dashboard")


@tech.route("/new-tech-ticket", methods=["GET", "POST"])
def tech_new_ticket():
    form=NewTicketForm()

    # Generate ticket number
    with current_app.app_context():
        latest_ticket = Ticket.query.order_by(Ticket.ticket_id.desc()).first()
        if latest_ticket:
            form.ticket_number.data = latest_ticket.ticket_id + 1
        else:
            form.ticket_number.data = 1


    # Get current UTC time
    current_datetime = datetime.now(timezone.utc)

    if form.validate_on_submit():
        try:
            # ticket_number
            # form.generate_ticket_number()
            ticket_number = form.ticket_number.data
            ticket_branch = form.ticket_branch.data
            ticket_type = form.ticket_type.data
            category = form.category.data
            title = form.title.data
            ticket_details = form.ticket_details.data
            
            # password = form.password.data
            ticket = Ticket(
                ticket_id=ticket_number,
                ticket_branch=ticket_branch,
                ticket_type=ticket_type,
                ticket_category=category,
                ticket_title=title,
                ticket_details=ticket_details,
                submission_datetime=current_datetime
                )
            
            
            db.session.add(ticket)
            db.session.commit()
            
            flash(f'Ticket created successfully. Your ticket number is: {form.ticket_number.data}.', 'success')
            return redirect(url_for('tech.tech_dashboard'))
        except Exception as e:
            db.session.rollback()
            error_message = str(e)
            return render_template('register.html', form=form, error=error_message)
        
    return render_template("tech_add_ticket.html", title="ITicket - New Ticket", form=form)


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


@tech.route("/update-user", methods=["GET", "PUT", "POST"])
def update_user():
    search_form = SearchUserForm()
    update_form = UpdateUserForm()

    

    # Search for the user by username
    search_id = User.query.filter_by(id=search_form.user_id.data).first_or_404()
    search_name = User.query.filter_by(username=search_form.username.data).first_or_404()
    
    if search_id or search_name:
        update_form.user_name.data = user.employee_name
        update_form.email.data = user.email
        update_form.user_type.data = user.role_type
        update_form.user_department.data = user.department
        update_form.user_job.data = user.job_title
        update_form.user_branch.data = user.branch
        update_form.user_status.data = user.user_status



    return render_template("tech_update_user.html", title="ITicket - User Dashboard", search_form=search_form, update_form=update_form)


@tech.route("/all-users", methods=["GET", "POST"])
def all_users():
    users = User.query.all()
    return render_template("tech_all_users.html", title="ITicket - All Users", users=users)
