# type: ignore
from flask import render_template, redirect, request, url_for, flash
from . import non_tech
from flask_login import login_user, logout_user, login_required, current_user
from ..models import Ticket
from .forms import NewTicketForm


@non_tech.route("/new-ticket", methods=["GET", "POST"])
def non_tech_new_ticket():
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
    
    return render_template("non-tech_add_ticket.html", title="ITicket - New Ticket", form=form)

@non_tech.route("/all-tickets")
def all_ticket():
    tickets = Ticket.query.all()
    return render_template("non-tech_all-tickets.html", title="ITicket - User Dashboard", form=form)