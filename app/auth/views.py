# type: ignore
from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.user_id.data).first()
        if user and user.check_password(password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            current_user_type = User.query.filter_by(role_type).first()
            current_user_name = User.query.filter_by(employee_name).first()

            if current_user_type == "tech":
                flash(f"Welcome {current_user_name}.", 'success')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('main.tech_dashboard'))
            
            elif current_user_type == "non-tech":
                flash(f"Welcome {current_user_name}.", 'success')
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                return redirect(url_for('main.all_ticket'))
        else:
            flash(f"Login Unsuccessful. Please check User ID and password", "dangerous")

    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))
