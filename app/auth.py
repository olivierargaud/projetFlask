from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

#####################
#### LOGIN ROUTE ####
#####################
@auth.route('/login/')
def login():
    return render_template('login.html')

######################
#### SIGNUP ROUTE ####
######################
@auth.route('/signup/')
def signup():
    return render_template('signup.html')

######################
#### LOGOUT ROUTE ####
######################
@auth.route('/logout/')
def logout():
    ## Logout the user ##
    logout_user()

    ## Delete the email user cookie ##
    session.pop("email", None)

    ## Then redirect to the main page ##
    return redirect(url_for('main.index'))

@auth.route('/signup/', methods=['POST'])
def signup_post():
    ## Store the email, name of the user and password in variables thanks to a form ##
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    ## Recover the email input by the user and compare it with the emails in database. Store it in a variable ##
    user = User.query.filter_by(email=email).first()
    
    ## So, if the email input by the user is equals to an email in the database, we flash and error message. Then reload the page ##
    if user:
        flash('This email is already used')
        return redirect(url_for('auth.signup'))

    ## Thanks to SQLAlchemy we created an user in database this way ##
    ## We obviously hash the password ##
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    ## Add table to our database and commit it ##
    db.session.add(new_user)
    db.session.commit()

    ## Redirect to login page ##
    return redirect(url_for('auth.login'))

@auth.route('/login/', methods=['POST'])
def login_post():
    ## Store the email and password in variables thanks to a form ##
    email = request.form.get('email')
    password = request.form.get('password')

    ## Check if the user actually exists ##
    user = User.query.filter_by(email=email).first()

    
    ## Take the user-supplied password, hash it, and compare it to the hashed password in the database ##
    if not user or not check_password_hash(user.password, password):
        flash('Email or password are false, please ty again')
        ## if the user doesn't exist or password is wrong, reload the page ##
        return redirect(url_for('auth.login'))

    ## Store users's email in 'email' varaible ##
    session["email"] = email
    ## If the above check passes, then we know the user has the right credentials ##
    login_user(user)

    ## Redirect to profile page ##
    return redirect(url_for('main.profile'))