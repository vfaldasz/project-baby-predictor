from jinja2 import StrictUndefined

import os

from flask import (Flask, render_template, redirect, request, flash, session, url_for,send_from_directory)
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.utils import secure_filename

from model import User, Photo, db, connect_to_db

UPLOAD_FOLDER = 'upload'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




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


@app.route("/prior_users")
def user_choice():
    """Show user choice to create new project or see pre-existing project"""

    return render_template("prior_users.html")

@app.route("/register_form", methods= ["GET"])
def register_form():


    return render_template("register_form.html")


@app.route("/register_form", methods = ["POST"])
def register_process():
    
    email = request.form.get("email")
    password = request.form.get("password")

# first, check if email is already in the database.
# don't allow a user to create a second record with the same email.

    #user_email = User.query.filter_by(email = "email").first()
    user = User.query.filter_by(email = email).first()

    if user:
        flash("User already exists. Please log-in.")
        return redirect('/login_form')
    else: 
        user_add = User(email= email, password= password)#adding user into dB
        db.session.add(user_add)
        db.session.commit()
        return redirect("/new_project")

@app.route("/login_form")
def login_form():

    return render_template("login_form.html")

@app.route("/login_form", methods = ["POST"])
def logged_in():

    email = request.form.get("email") #get email and password from log in form
    password = request.form.get("password")

    user = User.query.filter_by(email = email).first() #query dB to see if email is already there in dB. If so, flask returns the queried data back to us as our object. The object can then be used for later use (i.e user.password)

    if not user:
        flash("No such user")
        return redirect("/login_form")

    if user.password == password: 
        session['user_id']= user.user_id
        return redirect('/prior_users')
    else:
        flash("Incorrect password")
        return redirect("/login_form")

@app.route("/logged_out")
def logged_out():
    
    session.pop('user_id')
    flash("Logged-out")
    

    return redirect('/')

@app.route("/new_project")
def new_project():
    """submit photos and display results"""

    #photo_from db= Photo.query.all() #query photos from db and put into HTML
    return render_template("new_project.html")

@app.route("/results")
def old_projects():
    """show user's old projects"""

    return render_template("results.html")


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/form-data', methods=['POST'])
def upload_file():
    
    #check if the post request has the file part
    if 'file' not in request.files: #request from browser. 
        flash('No file part')
        return redirect('new_project')
    file = request.files['file'] # request.file similar to request.get/.args, in this case it is requesting a file from our html. If file exists, flask returns the queried file back to us as our object. The object can then be used for later use (i.e file.filename)
    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        flash('No selected file')
        return redirect('/new_project')
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)#make sure file is secure
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))#/uploads/name.jpeg
        return redirect('/new_project')#place holder for now. want morphed picture to show up on results page   
        #                         filename=filename))


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    #connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(port=5000, host='0.0.0.0')

