from flask import Flask,render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseRandomDice.db'
db = SQLAlchemy(app)


class dice(db.Model):
    """ table qui definit les dés """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    value = db.Column(db.Integer, nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Dé %r %r>' % (self.name , self.value)


class dice_group(db.Model):
    """ table qui definit les groupe de dés (lancer plusieurs dés) """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    children = db.relationship("dice_list_group")

    def __repr__(self):
        return '<groupe %r>' % (self.name)


class dice_list_group(db.Model):
    """ table de liaison entre les dés et les groupes de dés """
    id = db.Column(db.Integer, primary_key = True)
    idDice = db.Column(db.Integer)
    idGroup = db.Column(db.Integer, ForeignKey('dice_group.id'))
    
    def __repr__(self):
        return '<idDice %r %r>' % (self.idDice , self.idGroup)




class user(db.Model):
    """ table qui definit les utilisateurs """
    login = db.Column(db.String(200), nullable = False , primary_key = True)
    mdp = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)


    def __repr__(self):
        return '<User %r >' % self.name 


@app.route('/')
def loginDeBase():
     return render_template('login.html')

@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        return render_template('login.html')  
    else:
        return redirect('/')

@app.route('/login',methods=['POST','GET'])
def validerLogin():
    # if request.method == 'POST':
    #     username = request.form['login']
    #     password = request.form['mdp']
    #     error = None
    #     user = db.execute('SELECT * FROM user WHERE login = ?', (username,)).fetchone()

    #     if user is None:
    #         error = 'Incorrect username.'
    #     elif not check_password_hash(user['password'], password):
    #         error = 'Incorrect password.'

    #     if error is None:
    #         session.clear()
    #         session['user_id'] = user['id']
    #         return redirect(url_for('index'))

    #     flash(error)

    return render_template('pagePrincipale.html')

@app.route('/nouveauCompte')
def nouveauCompteDeBase():
    return render_template('nouveauCompte.html')

@app.route('/nouveauCompte',methods=['POST','GET'])
def nouveauCompte():
    if request.method == 'POST':
        return render_template('nouveauCompte.html')  
    else:
        return redirect('/')

@app.route('/validerNouveauCompte',methods=['POST','GET'])
def validerNouveauCompte():
    if request.method == 'POST':

        print (request.form['login'])
        print (request.form['mdp'])
        print (request.form['mdp2'])

        loginSaisie = request.form['login']
        mdpSaisie = request.form['mdp']
        confirmationMdpSaisie = request.form['mdp2']

        if mdpSaisie == confirmationMdpSaisie:

            new_user = user(login=loginSaisie,mdp = generate_password_hash(mdpSaisie))

            try:
                db.session.add(new_user)
                db.session.commit()
                return render_template('pagePrincipale.html')

            except:
                return redirect('/nouveauCompte')
        else:
            return redirect('/nouveauCompte')
    else:
        return redirect('/')