# type: ignore
from flask import Flask, render_template, url_for, flash

# below is another way to integrate "Bootstrap" into out app
# from flask_bootstrap import Bootstrap

app = Flask(__name__)

# below is another way to integrate "Bootstrap" into out app
# bootstrap = Bootstrap(app)


@app.route('/')
@app.route("/home")
def home():
    return render_template("testbootstrap.html")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', title="ITicket - Page not found"), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', title="Internal server error"), 500


if __name__ == '__main__':
    app.run(debug=True)