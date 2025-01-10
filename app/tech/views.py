# type: ignore
from flask import render_template, redirect, request, url_for, flash, current_app
from . import tech
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User, Ticket, IT, UserTicket
from .forms import NewUserForm, SearchTicketForm, SearchUserForm, NewTicketForm, UpdateUserForm
from .. import db
from datetime import datetime, timezone
from sqlalchemy import or_, update

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
            user = User(employee_id = user_id, employee_name=user_name, department=user_department, job_title=user_job, role_type=user_type, email=email, branch=user_branch, user_status=user_status)
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

    user_search = None

    if search_form.validate_on_submit():
        if search_form.user_id.data:
            user_search = User.query.filter_by(id=search_form.user_id.data).first()
        elif search_form.username.data:
            user_search = User.query.filter_by(employee_name=search_form.username.data).first()

        if user_search:
            update_form.user_name.data = user_search.employee_name
            update_form.email.data = user_search.email
            update_form.user_type.data = user_search.role_type
            update_form.user_department.data = user_search.department
            update_form.user_job.data = user_search.job_title
            update_form.user_branch.data = user_search.branch
            update_form.user_status.data = user_search.user_status
        else:
            flash("User not found", "danger")

    if update_form.validate_on_submit():
        if user_search:
            user_search.employee_name = update_form.user_name.data
            user_search.email = update_form.email.data
            if update_form.password.data:
                user_search.set_password(update_form.password.data)
            user_search.role_type = update_form.user_type.data
            user_search.department = update_form.user_department.data
            user_search.job_title = update_form.user_job.data
            user_search.branch = update_form.user_branch.data
            user_search.user_status = update_form.user_status.data

            user = User(
                employee_name=update_form.user_name.data,
                email=update_form.email.data,
                role_type=update_form.user_type.data,
                department=update_form.user_department.data

            )

            db.session.commit()
            flash("User updated successfully", "success")
            return redirect(url_for("tech.all_users"))



    return render_template("tech_update_user.html", title="ITicket - User Dashboard", search_form=search_form, update_form=update_form)


@tech.route("/all-users", methods=["GET", "POST"])
def all_users():
    users = User.query.all()
    return render_template("tech_all_users.html", title="ITicket - All Users", users=users)





class UserForm:
    def __init__(self):
        self.form = UpdateUserForm()
        self.form.user_id.data = ""
        self.form.user_name.data = ""
        self.form.email.data = ""
        self.form.user_type.data = ""
        self.form.user_department.data = ""
        self.form.user_job.data = ""
        self.form.user_branch.data = ""
        self.form.user_status.data = ""

    def get_form(self):
        return self.form

    def update_form_data(self, data):
        self.form.user_id.data = data.get('employee_id', "")
        self.form.user_name.data = data.get('employee_name', "")
        self.form.email.data = data.get('email', "")
        self.form.user_type.data = data.get('role_type', "")
        self.form.user_department.data = data.get('department', "")
        self.form.user_job.data = data.get('job_title', "")
        self.form.user_branch.data = data.get('branch', "")
        self.form.user_status.data = data.get('user_status', "")

class SearchUser(UserForm):
    def search_by_id(self):
        if self.form.user_id.data:
            id = int(self.form.user_id.data)
            print(f"Searching for user with ID: {id}")
            find_user = User.query.filter_by(employee_id=id).first()
            if find_user:
                print(f"Found user: {find_user.employee_name}")
                user_data = {
                    'employee_id': find_user.employee_id,
                    'employee_name': find_user.employee_name,
                    'email': find_user.email,
                    'role_type': find_user.role_type,
                    'department': find_user.department,
                    'job_title': find_user.job_title,
                    'branch': find_user.branch,
                    'user_status': find_user.user_status
                }
                self.update_form_data(user_data)
                return True
            else:
                print(f"No user found with ID: {id}")
        return False

class UpdateUser(UserForm):
    def update(self):
        if self.form.user_name.data and self.form.email.data and self.form.user_type.data and self.form.user_department.data and self.form.user_job.data and self.form.user_branch.data and self.form.user_status.data:
            user = User.query.filter_by(employee_id=self.form.user_id.data).first()
            if user:
                user.employee_id = self.form.user_id.data
                user.employee_name = self.form.user_name.data
                user.email = self.form.email.data
                user.role_type = self.form.user_type.data
                user.job_title = self.form.user_job.data
                user.department = self.form.user_department.data
                user.branch = self.form.user_branch.data
                user.user_status = self.form.user_status.data

                db.session.commit()
                flash("User updated successfully", "success")
                return redirect(url_for('tech.all_users'))
        flash("No user data found to update", "warning")
        return None

@tech.route("/test-update-user", methods=["GET", "PUT", "POST"])
def test_update_user():
    parent_form = UserForm()
    search_user = SearchUser()
    update_user = UpdateUser()
    
    if request.method == "POST":
        search_user.form.user_id.data = request.form['user_id']
        print(f"Entered user ID: {search_user.form.user_id.data}")
        
        if search_user.search_by_id():
            print("User found!")
            print(f"Retrieved user data: {search_user.form.__dict__}")
            parent_form.update_form_data(search_user.form.data)
            update_user.update_form_data(parent_form.form.data)
            
            # Perform the update
            update_result = update_user.update()
            if update_result:
                return update_result
            else:
                flash("Update failed", "danger")
        else:
            print("User not found")
            flash("User not found", "danger")
    
    return render_template("test_tech_update_user.html", 
                           title="ITicket - User Dashboard", 
                           form=search_user.form, current_user=None)






# class UserForm:
#     def __init__(self):
#         self.form = UpdateUserForm()
#         self.form.user_id.data = ""
#         self.form.user_name.data = ""
#         self.form.email.data = ""
#         self.form.user_type.data = ""
#         self.form.user_department.data = ""
#         self.form.user_job.data = ""
#         self.form.user_branch.data = ""
#         self.form.user_status.data = ""

#     def get_form(self):
#         return self.form

# class SearchUser(UserForm):
#     def search_by_id(self):
#         if self.form.user_id.data:
#             id = int(self.form.user_id.data)
#             print(f"Searching for user with ID: {id}")
#             find_user = User.query.filter_by(employee_id=id).first()
#             if find_user:
#                 print(f"Found user: {find_user.employee_name}")
#                 self.form.user_id.data = find_user.employee_id
#                 self.form.user_name.data = find_user.employee_name
#                 self.form.email.data = find_user.email
#                 self.form.user_type.data = find_user.role_type
#                 self.form.user_department.data = find_user.department
#                 self.form.user_job.data = find_user.job_title
#                 self.form.user_branch.data = find_user.branch
#                 self.form.user_status.data = find_user.user_status
#                 return True
#             else:
#                 print(f"No user found with ID: {id}")
#         return False

# class UpdateUser(UserForm):
#     def update(self):
#         if self.form.user_name.data and self.form.email.data and self.form.user_type.data and self.form.user_department.data and self.form.user_job.data and self.form.user_branch.data and self.form.user_status.data:
#             user = User.query.filter_by(employee_id=self.form.user_id.data).first()
#             if user:
#                 user.employee_id = self.form.user_id.data
#                 user.employee_name = self.form.user_name.data
#                 user.email = self.form.email.data
#                 user.role_type = self.form.user_type.data
#                 user.job_title = self.form.user_job.data
#                 user.department = self.form.user_department.data
#                 user.branch = self.form.user_branch.data
#                 user.user_status = self.form.user_status.data

#                 db.session.commit()
#                 flash("User updated successfully", "success")
#                 return redirect(url_for('tech.all_users'))
#         flash("No user data found to update", "warning")
#         return None

# @tech.route("/test-update-user", methods=["GET", "PUT", "POST"])
# def test_update_user():
#     search_user = SearchUser()
#     update_user = UpdateUser()
    
#     if request.method == "POST":
#         search_user.form.user_id.data = request.form['user_id']
#         print(f"Entered user ID: {search_user.form.user_id.data}")
        
#         if search_user.search_by_id():
#             print("User found!")
#             print(f"Retrieved user data: {search_user.form.__dict__}")
#             update_user.form = search_user.form
#             if update_user.update():
#                 return update_user.update()
#         else:
#             print("User not found")
#             flash("User not found", "danger")
    
#     return render_template("test_tech_update_user.html", 
#                            title="ITicket - User Dashboard", 
#                            form=search_user.form)



# class TestUpdateUser:
#     def __init__(self):
#         self.form = UpdateUserForm()
#         self.form.user_id.data = ""
#         self.form.user_name.data = ""
#         self.form.email.data = ""
#         self.form.password.data = ""
#         self.form.user_type.data = ""
#         self.form.user_department.data = ""
#         self.form.user_job.data = ""
#         self.form.user_branch.data = ""
#         self.form.user_status.data = ""

#     def search_by_id(self):
#         if self.form.user_id.data:
#             id = int(self.form.user_id.data)
#             print(f"Searching for user with ID: {id}")
#             find_user = User.query.filter_by(employee_id=id).first()
#             if find_user:
#                 print(f"Found user: {find_user.employee_name}")
#                 self.form.user_id.data = find_user.employee_id
#                 self.form.user_name.data = find_user.employee_name
#                 self.form.email.data = find_user.email
#                 self.form.user_type.data = find_user.role_type
#                 self.form.user_job.data = find_user.job_title
#                 self.form.user_department.data = find_user.department
#                 self.form.user_branch.data = find_user.branch
#                 self.form.user_status.data = find_user.user_status
#                 return True
#             else:
#                 print(f"No user found with ID: {id}")
#         return False
    
#     def update(self):
#         if self.form.user_name.data and self.form.email.data and self.form.user_type.data and self.form.user_department.data and self.form.user_job.data and self.form.user_branch.data and self.form.user_status.data:
#             user = User.query.filter_by(employee_id=self.form.user_id.data).first()
#             if user:
#                 user.employee_id = self.form.user_id.data
#                 user.employee_name = self.form.user_name.data
#                 user.email = self.form.email.data
#                 user.role_type = self.form.user_type.data
#                 user.job_title = self.form.user_job.data
#                 user.department = self.form.user_department.data
#                 user.branch = self.form.user_branch.data
#                 user.user_status = self.form.user_status.data

#             db.session.commit()
#             flash("User updated successfully", "success")
#             return redirect(url_for('tech.all_users'))
#         flash("No user data found to update", "warning")
#         return None




# @tech.route("/test-update-user", methods=["GET", "PUT", "POST"])
# def test_update_user():
#     test_user = TestUpdateUser()
    
#     if request.method == "POST":
#         test_user.form.user_id.data = request.form['user_id']
#         print(f"Entered user ID: {test_user.form.user_id.data}")
        
#         if test_user.search_by_id():
#             print("User found!")
#             print(f"Retrieved user data: {test_user.form.__dict__}")
#             if test_user.update():
#                 return test_user.update()
#         else:
#             print("User not found")
#             flash("User not found", "danger")
    
#     return render_template("test_tech_update_user.html", 
#                            title="ITicket - User Dashboard", 
#                            form=test_user.form)


#     # search_form =  SearchUserForm()
#     # form = UpdateUserForm()
#     # user_id = int(form.user_id.data)
#     # search_user_id = User.query.filter_by(employee_id=int(user_id)).first()
#     # print(f"search_user_id is: {search_user_id}")
#     # if search_user_id:
#     # def __init__(self):
#     #     self.form.user_id.data = ""
#     #     self.form.user_name.data = ""
#     #     self.form.email.data = ""
#     #     self.form.password.data = ""
#     #     self.form.user_type.data = ""
#     #     self.form.user_department.data = ""
#     #     self.form.user_job.data = ""
#     #     self.form.user_branch.data = ""
#     #     self.form.user_status.data = ""

#     # def search_by_id(self):
#     #     if self.form.user_id.data:
#     #         id = int(self.form.user_id.data)
#     #         find_user = User.query.filter_by(employee_id=id).first()
#     #         if find_user:
#     #             self.form.user_id.data = find_user.employee_id
#     #             self.form.user_name.data = find_user.employee_name
#     #             self.form.email.data = find_user.email
#     #             self.form.user_type.data = find_user.role_type
#     #             self.form.user_job.data = find_user.job_title
#     #             self.form.user_department.data = find_user.department
#     #             self.form.user_branch.data = find_user.branch
#     #             self.form.user_status.data = find_user.user_status
                    
#     # def update(self):
#     #     user = User.query.filter_by(employee_id=self.form.user_id.data).first()
#     #     if user:
#     #         user.employee_id = self.form.user_id.data
#     #         user.employee_name = self.form.user_name.data
#     #         user.email = self.form.email.data
#     #         user.role_type = self.form.user_type.data
#     #         user.job_title = self.form.user_job.data
#     #         user.department = self.form.user_department.data
#     #         user.branch = self.form.user_branch.data
#     #         user.user_status = self.form.user_status.data

#     #         db.session.commit()
#     #         flash("User updated successfully", "success")
#     #         return redirect(url_for('tech.all_users'))
    
#     # if search_by_id():
#     #     update()



#     # # If the form is not submitted or there's an error, render the form with empty data
#     # return render_template("test_tech_update_user.html", 
#     #                        title="ITicket - User Dashboard", 
#     #                        form=form)
