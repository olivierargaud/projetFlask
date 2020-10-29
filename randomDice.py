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


class dice(db.Model):
    """ table qui definit les dés """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    value = db.Column(db.Integer, nullable = False)
    last_result = db.Column(db.Integer)
    owner = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    group = db.relationship('dice_list_group', backref=db.backref('dice', lazy='joined'))

    def __repr__(self):
        return '<Dé %r %r>' % (self.name , self.value)


class dice_group(db.Model):
    """ table qui definit les groupe de dés (lancer plusieurs dés) """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    owner = db.Column(db.String(50), nullable = False)
    last_result = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<groupe %r>' % (self.name)


class dice_list_group(db.Model):
    """ table de liaison entre les dés et les groupes de dés """
    id = db.Column(db.Integer, primary_key = True)
    idDice = db.Column(db.Integer, ForeignKey('dice.id'))
    idGroup = db.Column(db.Integer, ForeignKey('dice_group.id'))
    last_result = db.Column(db.Integer)
    
    def __repr__(self):
        return '<idDice %r idGroup %r>' % (self.idDice , self.idGroup)


class user(db.Model):
    """ table qui definit les utilisateurs """
    login = db.Column(db.String(200), nullable = False , primary_key = True)
    mdp = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<User %r >' % self.login 




@app.route('/',methods=['POST','GET'])
def login():
        return render_template('login.html')  
   

@app.route('/login',methods=['POST','GET'])
def validerLogin():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['mdp']
        print(username)
        print(password)
       
        utilisateurEnBase = user.query.filter_by(login = username).first()

        if utilisateurEnBase:
            if check_password_hash(utilisateurEnBase.mdp, password):
                session['username'] = username
                
                return redirect('/pagePrincipale')
            else:
                return redirect('/')
        else:
            return redirect('/')
    else:
            return redirect('/')

@app.route('/logout',methods=['POST','GET'])
def logout():
    if request.method == 'POST':

        session.pop('username', None)
        return redirect('/')
    else:
            return redirect('/')


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
                return redirect('/')

            except:
                return redirect('/nouveauCompte')
        else:
            return redirect('/nouveauCompte')
    else:
        return redirect('/')




@app.route('/pagePrincipale',methods=['POST','GET'])
def pagePrinc():
    if request.method == 'POST':

        listeDe = dice.query.filter(dice.owner == session['username']).all()
        listeLance = dice_group.query.filter(dice_group.owner == session['username']).all()
        return render_template('pagePrincipale.html', listeDe=listeDe , listeLance=listeLance ,utilisateurActif = session['username'])
    else:
        if 'username' in session:
            listeDe = dice.query.filter(dice.owner == session['username']).all()
            listeLance = dice_group.query.filter(dice_group.owner == session['username']).all()
            return render_template('pagePrincipale.html', listeDe=listeDe , listeLance=listeLance ,utilisateurActif = session['username'])
        else:
            return redirect('/')





@app.route('/creationDe',methods=['POST','GET'])
def creationDe():
    
    listeDe = dice.query.filter(dice.owner == session['username']).all()
    return render_template('creationDe.html', listeDe=listeDe ,utilisateurActif = session['username'])
   



@app.route('/valideDe',methods=['POST','GET'])
def validerDe():
    if request.method == 'POST':

        print (request.form['nomDuDe'])
        print (request.form['nbDeFace'])
       

        new_dice = dice(name=request.form['nomDuDe'],value = request.form['nbDeFace'])
        new_dice.owner = session['username']
        

        try:
            db.session.add(new_dice)
            db.session.commit()
            
            return redirect('/creationDe')

        except:
            return redirect('/creationDe')

       
        return redirect('/creationDe')
    else:
        return redirect('/creationDe')



@app.route('/suprimerDe/<int:id>',methods=['POST','GET'])
def suprimeDe(id):
    dice_to_delete = dice.query.get_or_404(id)

    try:
        db.session.delete(dice_to_delete)
        db.session.commit()
        return redirect('/creationDe')
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


@app.route('/lancer/<int:id>',methods=['POST','GET'])
def lancer(id):
    dice_to_launch = dice.query.get_or_404(id)

    dice_to_launch.last_result = random.randint (1,dice_to_launch.value)
    print(dice_to_launch.last_result)
    db.session.commit()
    
    return redirect('/pagePrincipale')




@app.route('/creationLance',methods=['POST','GET'])
def creationLance():
    if request.method == 'POST':
        listeLance = dice_group.query.filter(dice_group.owner == session['username']).all()
        return render_template('creationLance.html', listeLance=listeLance , utilisateurActif = session['username'])
        return redirect('/')


@app.route('/validerLance',methods=['POST','GET'])
def validerLance():
    if request.method == 'POST':

        print (request.form['nomDuLance'])
     
        new_dice_group = dice_group(name=request.form['nomDuLance'])
        new_dice_group.owner = session['username']
        
        try:
            db.session.add(new_dice_group)
            db.session.commit()
            
            return redirect('/pagePrincipale')

        except:
            return redirect('/creationLance')
      
        return redirect('/pagePrincipale')
    else:
        return redirect('/')



@app.route('/suprimerLance/<int:id>',methods=['POST','GET'])
def suprimeLance(id):
    dice_group_to_delete = dice_group.query.get_or_404(id)

    try:
        db.session.delete(dice_group_to_delete)
        db.session.commit()
        return redirect('/pagePrincipale')
    except:
        return 'delete problem'



@app.route('/parametrerLance/<int:id>',methods=['POST','GET'])
def parametrerLance(id):
    
    groupeSelectionne = dice_group.query.get_or_404(id)
    session['idGroupeSelectionne'] = id
    
    listeDe = dice.query.filter(dice.owner == session['username']).all()
    print(listeDe)
    listeDeGroupe = dice.query.filter(dice.group.any(dice_list_group.idGroup == groupeSelectionne.id)).all()
    print(dice.query.filter(dice.group.any(dice_list_group.idGroup == groupeSelectionne.id)))
    print(listeDeGroupe)

    listeJonction = dice_list_group.query.filter(dice_list_group.idGroup == groupeSelectionne.id).all()
    print(listeJonction)
    
    return render_template('parametrageLance.html', listeDe=listeDe , listeDeGroupe=listeDeGroupe , listeJonction=listeJonction , utilisateurActif = session['username'] , groupeSelectionne = groupeSelectionne)


@app.route('/ajouterAuLance/<int:id>',methods=['POST','GET'])
def ajouterDe(id):
    dice_to_add = dice.query.get_or_404(id)
    group_to_add_dice = dice_group.query.get_or_404(session['idGroupeSelectionne'])

    new_dice_list_group = dice_list_group( idDice=dice_to_add.id , idGroup=group_to_add_dice.id )
    
    db.session.add(new_dice_list_group)
    db.session.commit()
      
    print(new_dice_list_group)

    return redirect(url_for('parametrerLance', id=session['idGroupeSelectionne']))


@app.route('/enleverAuLance/<int:id>',methods=['POST','GET'])
def enleverDe(id):
    # dice_to_remove = dice.query.get_or_404(id)
    # group_to_remove_dice = dice_group.query.get_or_404(session['idGroupeSelectionne'])

    dice_list_group_to_remove = dice_list_group.query.get_or_404(id)

    db.session.delete(dice_list_group_to_remove)
    db.session.commit()
      
    return redirect(url_for('parametrerLance', id=session['idGroupeSelectionne']))





@app.route('/lancerGroupe/<int:id>',methods=['POST','GET'])
def lancerGroup(id):
    # declaration et initialisation de la variable resultat du lancé
    resultatLance = 0
    # recuperation du groupe sur lequel effectuer le lancé
    dice_group_to_launch = dice_group.query.get_or_404(id)
    # list des jonction du groupe selectionné
    listeJonction = dice_list_group.query.filter(dice_list_group.idGroup == dice_group_to_launch.id).all()
   
   
   
    for jonction in listeJonction:
        print (jonction.id)
        deSelect = dice.query.filter(dice.id == jonction.idDice).first()
        print (deSelect.name)
        dice_result = random.randint (1,deSelect.value)
        resultatLance += dice_result
        print('resultat individuel ' + str(dice_result))


    
    print('resultat total ' + str(resultatLance))
    dice_group_to_launch.last_result = resultatLance
    db.session.commit()

    
    return redirect('/pagePrincipale')