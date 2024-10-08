# type: ignore
from flask import Flask, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from forms import LoginForm
import os
from models import Ticket, IT, User, Role, UserTicket, RoleType, TicketStatus, TicketType, Requests


# below is another way to integrate "Bootstrap" into out app
# from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")
# below is another way to integrate "Bootstrap" into out app
# bootstrap = Bootstrap(app)

# configure session 
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure the database using mysql database for production
# app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.environ.get('DEV_USER')}:{os.environ.get('DEV_PASSWORD')}@localhost/{os.environ.get('FULL_TICKETTREK_DEV_DB')}"

# configure the database using sqlite database for development
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"



#create the database instance
db = SQLAlchemy(app)



@app.route('/')
@app.route("/home")
def home():
    return render_template("test_home.html", title="ITicket - Home")


@app.route("/login", methods=["GET", "POST"])
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="ITicket - Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title="Internal server error"), 500


if __name__ == '__main__':
    app.run(debug=True)