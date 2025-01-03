# type: ignore
from flask import render_template, redirect, request, url_for, flash
from . import non_tech
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from .forms import NewTicketForm


@non_tech.route("/new-ticket", methods=["GET", "POST"])
def non_tech_new_ticket():
    return render_template("non-tech_add_ticket.html", title="ITicket - New Ticket")

@non_tech.route("/all-tickets")
def all_ticket():
    return render_template("non-tech_all-tickets.html", title="ITicket - User Dashboard")