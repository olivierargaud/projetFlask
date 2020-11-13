from flask import Blueprint, render_template, session, request, redirect, url_for
from random import randrange
from flask_login import login_required, current_user
from .models import Des
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile/')
def profile():
    if "email" in session:

        email = session["email"]

        dice_user = []
        dice_user = Des.query.filter_by(NomProprietaire=current_user.name).all()

        return render_template('profile.html', name=current_user.name, dice_user=dice_user)

@main.route('/newDice', methods=['POST'])
def creationDe():
    email = session["email"]
    name = current_user.name
    NumberOfFaces = request.form.get('NumberOfFaces')
    DiceName = request.form.get('DiceName')
    new_des = Des(NbrDeFace=NumberOfFaces, NomDuDes=DiceName, Proprietaire=email, NomProprietaire=name, LastResult="0")

    db.session.add(new_des)
    db.session.commit()

    return redirect(url_for('main.profile'))

@main.route('/deleteDice', methods=['POST'])
def deleteDice():
    getIdDiceToDelete = request.form.get('getIdDiceToDelete')
    diceToDelete = Des.query.filter_by(id=getIdDiceToDelete).first()
    db.session.delete(diceToDelete)
    db.session.commit()

    return redirect(url_for('main.profile'))

@main.route('/randomDice', methods=['POST'])
def randomDice():
    getNumberForRandom = request.form.get('getNumberForRandom')
    diceToRandom = Des.query.filter_by(id=getNumberForRandom).first()
    diceToRandom = diceToRandom.NbrDeFace
    randomResult = randrange(0, int(diceToRandom)+1)
    LastResult = randomResult
    diceToRandom = Des.query.filter_by(id=getNumberForRandom).first()
    diceToRandom.LastResult = LastResult
    db.session.commit()
    return redirect(url_for('main.profile'))
