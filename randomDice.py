from flask import Flask,render_template, request, redirect, session, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
import random


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baseRandomDice.db'
app.secret_key = 'maSuperClefSecrete'
db = SQLAlchemy(app)
utilisateurActif =""


class dice(db.Model):
    """ table qui definit les dés """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    value = db.Column(db.Integer, nullable = False)
    last_result = db.Column(db.Integer)
    owner = db.Column(db.String(200), nullable = False)
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
        return '<User %r >' % self.login 


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
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['mdp']
        print(username)
        print(password)
        flash("test flash")
        error = None
        utilisateurEnBase = user.query.filter_by(login = username).first()
        if utilisateurEnBase:
            if check_password_hash(utilisateurEnBase.mdp, password):
                utilisateurActif = utilisateurEnBase.login
                print(utilisateurActif)
                listeDe = dice.query.order_by(dice.name).all()
                return render_template('pagePrincipale.html', listeDe=listeDe ,utilisateurActif = utilisateurActif)
            else:
                return redirect('/')
            # return render_template('pagePrincipale.html')
        else:
            flash("test flash 2")
        utilisateur = user.query.filter_by().first()
        print(utilisateur)
        
        motdepass = user.query.filter_by().first().mdp
        print(motdepass)

        # utilisateur = db.Query.from_statement(db,'SELECT * FROM user WHERE login = logintest')
        # user = db.execute('SELECT * FROM user WHERE login = ?', (username,)).fetchone()

        # session.query(User).from_statement(text("SELECT * FROM users where name=:name")).params(name='ed').all()

        # if utilisateur is None:
        #     error = 'Incorrect username.'
        # elif not check_password_hash(utilisateur['password'], password):
        #     error = 'Incorrect password.'

        # if error is None:
        #     session.clear()
        #     session['user_id'] = utilisateur['id']
        #     return redirect(url_for('pagePrincipale'))

        # flash(error)

    

# @app.route('/nouveauCompte')
# def nouveauCompteDeBase():
#     return render_template('nouveauCompte.html')

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



@app.route('/creationDe',methods=['POST','GET'])
def creationDe():
    if request.method == 'POST':
        return render_template('creationDe.html')  
    else:
        return redirect('/')




@app.route('/valideDe',methods=['POST','GET'])
def validerDe():
    if request.method == 'POST':

        print (request.form['nomDuDe'])
        print (request.form['nbDeFace'])
       

        new_dice = dice(name=request.form['nomDuDe'],value = request.form['nbDeFace'])

        try:
            db.session.add(new_dice)
            db.session.commit()
            listeDe = dice.query.order_by(dice.name).all()
            return render_template('pagePrincipale.html', listeDe=listeDe )

        except:
            return redirect('/nouveauCompte')

       
        return redirect('/pagePrincipale')
    else:
        return redirect('/')



@app.route('/delete/<int:id>')
def delete(id):
    dice_to_delete = dice.query.get_or_404(id)

    try:
        db.session.delete(dice_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'delete problem'


@app.route('/update/<int:id>',methods = ["GET",'POST'])
def update(id):
    dice_to_update = dice.query.get_or_404(id)


    if request.method == 'POST':

        dice_to_update.name = request.form['nomDuDe']
        dice_to_update.value = request.form['nbDeFace']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'probleme dans la validation de l update'

    else:
        return render_template('update.html',dice = dice_to_update)


@app.route('/lancer/<int:id>')
def lancer(id):
    dice_to_launch = dice.query.get_or_404(id)

    
    
    dice_to_launch.last_result = random.randint (1,dice_to_launch.value)
    print(dice_to_launch.last_result)
    db.session.commit()
    
    listeDe = dice.query.order_by(dice.name).all()
    return render_template('pagePrincipale.html', listeDe=listeDe)
