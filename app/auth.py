from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login/')
def login():
    return render_template('login.html')

@auth.route('/signup/')
def signup():
    return render_template('signup.html')

@auth.route('/logout/')
def logout():
    logout_user()
    session.pop("email", None)
    return redirect(url_for('main.index'))

@auth.route('/signup/', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    print(email, name, password)

    user = User.query.filter_by(email=email).first()

    if user:
        flash('Cet email existe déjà')
        return redirect(url_for('auth.signup'))

    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    print(new_user)

    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login/', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Informations de connexions erronées, veuillez réessayer.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    session["email"] = email
    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.profile'))