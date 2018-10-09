from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Photo

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users= User.query.all()
    if 'user_id' in session:
        print('User_id is {}:'.format(session['user_id']))

    return render_template("user_list.html", users=users)

@app.route("/register", methods= ["GET"])
def register_form():
    ###our awesome code!!

    return render_template("register_form.html")


@app.route("/register", methods = ["POST"])
def register_process():
    
    email = request.form.get("email")
    password = request.form.get("password")

    user_add = User(email= email, password= password)
    db.session.add(user_add)
    db.session.commit()


    return redirect("/")

@app.route("/login_form")
def login_form():

    return render_template("login_form.html")

@app.route("/login_form", methods = ["POST"])
def logged_in():

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email = email).first()

    if not user:
        flash("No such user")
        return redirect("/login_form")

    if user.password == password:
        session['user_id']= user.user_id
        return redirect('/users/{}'.format(user.user_id))
    else:
        flash("Incorrect password")
        return redirect("/login_form")

@app.route("/logged_out")
def logged_out():
    
    session.pop('user_id')
    flash("Logged-out")
    

    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    #connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')

