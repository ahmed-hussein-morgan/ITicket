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


    # Search by User ID
    search_by_id = User.query.filter_by(id=search_form.user_id.data).first()

    # Search by Username
    search_by_name = User.query.filter_by(employee_name=search_form.username.data).first()



    if not search_by_id and not search_by_name:
        flash(f"No user found with this User ID or User Name {search_form.username.data}", "danger")

    elif search_by_id:
        user_search_id = User.query.filter_by(id=search_form.user_id.data).first()
        print(f"ID - user_search_id = {user_search_id}")
    elif search_by_name:
        user_search_name = User.query.filter_by(employee_name=search_form.username.data).first().id
        print(f"ID - user_search_name : {user_search_name}")
    else:
        user_search_id = None

    # employee_query = db.session.query(User).filter(or_(
    # User.id == user_search_id,
    # User.employee_name == search_form.username.data
    # )).first().id

    # print(f"employee_query is {employee_query}")



    # elif search_by_id or search_by_name:
    #     user_search_id = User.query.filter(or_(User.id == search_by_id.id, User.employee_name == search_by_name.employee_name)).get(User.id)

    #     print(f"user_search_id = {user_search_id}")

    #     user_search_id = int(user_search_id)
    #     print(f"INT user_search_id = {user_search_id}")

    
    if update_form.validate_on_submit():
        try:
            # update_form.user_id.data = User.query.filter_by(id=employee_query).first().id
            # print(f"update_form.user_id.data = {update_form.user_id.data}")

            update_form.user_name.data = User.query.filter_by(id=employee_query).first().employee_name
            print(f"update_form.user_name.data = {update_form.user_name.data}")

            update_form.email.data = User.query.filter_by(id=employee_query).first().email
            print(f"update_form.email.data = {update_form.email.data}")

            update_form.user_type.data = User.query.filter_by(id=employee_query).first().role_type
            print(f"update_form.user_type.data = {update_form.user_type.data}")

            update_form.user_department.data = User.query.filter_by(id=employee_query).first().department
            print(f"update_form.user_department.data = {update_form.user_department.data}")

            update_form.user_job.data= User.query.filter_by(id=employee_query).first().job_title
            print(f"update_form.user_job.data = {update_form.user_job.data}")

            update_form.user_branch.data= User.query.filter_by(id=employee_query).first().branch
            print(f"update_form.user_branch.data = {update_form.user_branch.data}")

            update_form.user_status.data = User.query.filter_by(id=employee_query).first().user_status
            print(f"update_form.user_status.data = {update_form.user_status.data}")

            
            # password = form.password.data
            user = User(id=user_id, employee_name=user_name, department=user_department, job_title=user_job, role_type=user_type, email=email, branch=user_branch, user_status=user_status)
            
            if update_form.password.data:
                user.set_password(password)
            
            
            db.session.add(user)
            db.session.commit()
            
            flash(f'User updated successfully for {update_form.user_name.data}.', 'success')


            return redirect(url_for('tech.all_users'))
        except Exception as e:
            db.session.rollback()
            error_message = str(e)
            return render_template('register.html', search_form=search_form, update_form=update_form, error=error_message)
    return render_template("tech_update_user.html", title="ITicket - User Dashboard", search_form=search_form, update_form=update_form)


    # if search_by_id:
    #     update_form.user_id.data = search_by_id.id
    #     update_form.user_name.data = search_by_id.employee_name
    #     update_form.email.data = search_by_id.email
    #     update_form.user_type.data = search_by_id.role_type
    #     update_form.user_department.data = search_by_id.department
    #     update_form.user_job.data = search_by_id.job_title
    #     update_form.user_branch.data = search_by_id.branch
    #     update_form.user_status.data = search_by_id.user_status

    #     print(f"search by ID result is :{search_by_id.id}, {search_by_id.employee_name}, {search_by_id.email},\
    #           {search_by_id.role_type},{search_by_id.department}, {search_by_id.job_title},\
    #            {search_by_id.branch}, {search_by_id.user_status} ")


    # elif search_by_name:
    #     # If found by Username, try to get ID
    #     user_search_id = User.query.filter_by(employee_name=search_by_name.employee_name).first().id

    #     print(f" user_search_id : {user_search_id}")

    #     if user_search_id:
    #         update_form.user_id.data =  user_search_id
    #         update_form.user_name.data = search_by_name.employee_name
    #         update_form.email.data = search_by_name.email
    #         update_form.user_type.data = search_by_name.role_type
    #         update_form.user_department.data = search_by_name.department
    #         update_form.user_job.data = search_by_name.job_title
    #         update_form.user_branch.data = search_by_name.branch
    #         update_form.user_status.data = search_by_name.user_status

    #         print(f"search by ID result is :{user_search_id}, {search_by_name.employee_name}, {search_by_name.email},\
    #           {search_by_name.role_type},{search_by_name.department}, {search_by_name.job_title},\
    #            {search_by_name.branch}, {search_by_name.user_status} ")

    #     else:
    #         flash(f"No user found with name {search_form.username.data}", "danger")
    

    # else:
    #     flash(f"No user found with ID {search_form.user_id.data} or name {search_form.username.data}", "danger")



    # if update_form.validate_on_submit():
    #     try:
    #         user_id = update_form.user_id.data
    #         user_name = update_form.user_name.data
    #         email = update_form.email.data
    #         user_type = update_form.user_type.data
    #         user_department = update_form.user_department.data
    #         user_job =update_form.user_job.data
    #         user_branch = update_form.user_branch.data
    #         user_status = update_form.user_status.data
            
    #         # password = form.password.data
    #         user = User(id=user_id, employee_name=user_name, department=user_department, job_title=user_job, role_type=user_type, email=email, branch=user_branch, user_status=user_status)
            
    #         if update_form.password.data:
    #             user.set_password(password)
            
            
    #         db.session.add(user)
    #         db.session.commit()
            
    #         flash(f'User updated successfully for {update_form.user_name.data}.', 'success')


    #         return redirect(url_for('tech.all_users'))
    #     except Exception as e:
    #         db.session.rollback()
    #         error_message = str(e)
    #         return render_template('register.html', search_form=search_form, update_form=update_form, error=error_message)
    # return render_template("tech_update_user.html", title="ITicket - User Dashboard", search_form=search_form, update_form=update_form)

# Replace deleting the user by updating its status (Enable/Disable) to keep all users data.
#       "Delete" feature could be added into the next version when creating the "Manager" user_type.
# @tech.route("/delete-user", methods=["GET", "POST"])
# def delete_user():
#     return render_template("tech_delete_user.html", title="ITicket - User Dashboard")

@tech.route("/all-users", methods=["GET", "POST"])
def all_users():
    users = User.query.all()
    return render_template("tech_all_users.html", title="ITicket - All Users", users=users)
