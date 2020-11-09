from flask import Blueprint, render_template, session, request
from flask_login import login_required, current_user
from .models import Des
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile/')
def profile():
    print("toto")
    if "email" in session:
        
        email = session["email"]

        return render_template('profile.html', name=current_user.name)

@main.route('/creationDe', methods=['POST'])
def creationDe():
    email = session["email"]
    NbrDeFace = request.form.get('NbrDeFace')

    print(NbrDeFace)

    new_des = Des(NbrDeFace=NbrDeFace, Proprietaire=email)
    db.session.add(new_des)
    db.session.commit()
    return render_template('profile.html', name=current_user.name)