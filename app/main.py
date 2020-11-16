from flask import Blueprint, render_template, session, request, redirect, url_for
from random import randrange
from flask_login import login_required, current_user
from .models import Des
from . import db
import os

main = Blueprint('main', __name__)

## Index route, means that is the first page you get when you access to the website ##
@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

## Profile route, route you're redirected when you login ##
@main.route('/profile/')
def profile():
    ## Store the session data by user's email in the cookie ##
    if "email" in session:
        
        ## Store users's email in 'email' varaible ##
        email = session["email"]

        ## Create and make 'dice_user' variable as an array ##
        ## Recover all the recording in the table which matches with the user's dice ##
        ## We'll use it in the profile template to recover all the user's dice by id their ids ##
        dice_user = []
        dice_user = Des.query.filter_by(OwnerName=current_user.name).all()

        ## Return profile template and variables we'll use in this template ##
        return render_template('profile.html', name=current_user.name, dice_user=dice_user)


################################
#### ROUTE TO CREATE A DICE ####
################################
@main.route('/newDice', methods=['POST'])
def creationDe():
    ## Store the email, name of the user, number of dice faces and dice name in variables ##
    email = session["email"]
    name = current_user.name
    NumberOfFaces = request.form.get('NumberOfFaces')
    DiceName = request.form.get('DiceName')

    ## Thanks to SQLAlchemy we created a dice in database this way ##
    new_des = Des(NumberOfFaces=NumberOfFaces, DiceName=DiceName, Owner=email, OwnerName=name, LastResult="0")

    ## Add table to our database and commit it ##
    db.session.add(new_des)
    db.session.commit()
    
    ## Redirect to profile page ##
    return redirect(url_for('main.profile'))


################################
#### ROUTE TO DELETE A DICE ####
################################
@main.route('/deleteDice', methods=['POST'])
def deleteDice():
    ## Thanks to an unshown input which recover the dice, we can recover its id and store it in variable ##
    getIdDiceToDelete = request.form.get('getIdDiceToDelete')
    diceToDelete = Des.query.filter_by(id=getIdDiceToDelete).first()

    ## Thanks to SQLAlchemy again we delete a dice in database this way ##
    db.session.delete(diceToDelete)
    db.session.commit()

    ## Redirect to profile page ##
    return redirect(url_for('main.profile'))


################################
#### ROUTE TO ROLL THE DICE ####
################################
@main.route('/randomDice', methods=['POST'])
def randomDice():
    ## Thanks to an unshown input which recover the dice, we can recover its id and store it in variable ##
    getNumberForRandom = request.form.get('getNumberForRandom')
    diceToRandom = Des.query.filter_by(id=getNumberForRandom).first()

    ## We select the 'NumberOfFaces' number in database ##
    diceToRandom = diceToRandom.NumberOfFaces

    ## In randomResult 'variable' we store an random number between 1 (a dice can't return 0) and its number of faces ##
    ## 'randrange' function exclude the last value, so we add 1 to the number of faces##
    randomResult = randrange(1, int(diceToRandom)+1)

    ## We recover the recording the same way before ##
    ## We store random result in 'LastResult' recording in the database. Then we commit it ##
    diceToRandom = Des.query.filter_by(id=getNumberForRandom).first()
    diceToRandom.LastResult = randomResult
    db.session.commit()

    ## Redirect to profile page ##
    return redirect(url_for('main.profile'))