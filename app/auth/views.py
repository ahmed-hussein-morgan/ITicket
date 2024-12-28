# type: ignore
from flask import render_template, redirect, request, url_for, flash
from . import auth
from flask_login import login_user
from ..models import User
from .forms import LoginForm


@auth.route('/login', method=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=form.user_id.data).first()
        if user and user.check_password(password_hash, form.password.data):
            login_user(user, remember=form.remember.data)
            user_type = 
            

    return render_template('auth/login.html')