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



######################################################################################################################################################
#                                                           table base de donnée                                                                     #
######################################################################################################################################################


########################################################################################
#                                                                                      #
########################################################################################
class dice(db.Model):
    """ table qui definit les dés """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    value = db.Column(db.Integer, nullable = False)
    owner = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    group = db.relationship('dice_list_group', backref=db.backref('dice', lazy='joined'))

    def __repr__(self):
        return '<Dé %r , %r faces>' % (self.name , self.value)

########################################################################################
#                                                                                      #
########################################################################################
class dice_group(db.Model):
    """ table qui definit les groupes de dés (lancer plusieurs dés) """
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    owner = db.Column(db.String(50), nullable = False)
    last_result = db.Column(db.Integer)
    nb_de = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Lancé %r , %r dé(s)>' % (self.name,self.nb_de)

########################################################################################
#                                                                                      #
########################################################################################
class dice_list_group(db.Model):
    """ table de liaison entre les dés et les groupes de dés """
    id = db.Column(db.Integer, primary_key = True)
    idDice = db.Column(db.Integer, ForeignKey('dice.id'), nullable = False)
    idGroup = db.Column(db.Integer, ForeignKey('dice_group.id'), nullable = False)
    
    def __repr__(self):
        return '<idDice %r idGroup %r>' % (self.idDice , self.idGroup)

########################################################################################
#                                                                                      #
########################################################################################
class user(db.Model):
    """ table qui definit les utilisateurs """
    login = db.Column(db.String(200), nullable = False , primary_key = True)
    mdp = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<User %r >' % self.login 

########################################################################################
#                                                                                      #
########################################################################################
class historique_lance(db.Model):
    """ table qui stock l'historique des resultats des Lancés """
    id = db.Column(db.Integer, primary_key = True)
    lance_id = db.Column(db.Integer, ForeignKey('dice_group.id'), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<Historique db lancé %r >' % self.id 

########################################################################################
#                                                                                      #
########################################################################################
class historique(db.Model):
    """ table qui stock l'historique des resultats des dés """
    id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.Integer)
    de_id = db.Column(db.Integer, ForeignKey('dice.id'), nullable = False)
    historiqueLance_id = db.Column(db.Integer, ForeignKey('historique_lance.id'))
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<Historique db de id %r >' % self.id 



######################################################################################################################################################
#                                                           objet pour l'affichage                                                                   #
######################################################################################################################################################


########################################################################################
#                                                                                      #
########################################################################################
class historique_affichage():
    """ objet qui regroupe les informations a afficher """
    numero_lance = 0
    total_max = 0
    total = 0
    date_created = ''
    liste_detail = []

    def __repr__(self):
        return '<Historique numéro %r , %r / %r >' % (self.numero_lance , self.total , self.total_max) 

########################################################################################
#                                                                                      #
########################################################################################
class detail_de():
    """ objet qui regroupe les informations detaillé d'un dé a afficher"""
    nom = ''
    face = 0
    value = 0
    
    def __repr__(self):
        return '<Historique dé %r , %r / %r >' % (self.nom , self.value , self.face) 


######################################################################################################################################################
#                                                           fonction                                                                                 #
######################################################################################################################################################

########################################################################################
#                                                                                      #
########################################################################################
def testLogin():
    if 'username' in session:
        utilisateurActif = session['username']
    else:
        utilisateurActif = "aucun"
    return utilisateurActif



######################################################################################################################################################
#                                                           route                                                                                    #
######################################################################################################################################################

########################################################################################
#                               racine                                                 #
########################################################################################
@app.route('/',methods=['POST','GET'])
def login():
    page1 = "non_active"
    page2 = "non_active"
    page3 = "non_active"
    page4 = "active"
    utilisateurActif = testLogin()
    return render_template('login.html',utilisateurActif = utilisateurActif,page1=page1,page2=page2,page3=page3,page4=page4)  
   
########################################################################################
#                               commande login                                         #
########################################################################################
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
                flash("mauvais mot de passe")
                return redirect('/')
        else:
            flash("utilisateur inconnu")
            return redirect('/')
    else:
        return redirect('/')

########################################################################################
#                               commande logout                                        #
########################################################################################
@app.route('/logout',methods=['POST','GET'])
def logout():
        session.pop('username', None)
        return redirect('/')
  

########################################################################################
#                               affichage page nouveau compte                          #
########################################################################################
@app.route('/nouveauCompte',methods=['POST','GET'])
def nouveauCompte():
    page1 = "non_active"
    page2 = "non_active"
    page3 = "non_active"
    page4 = "non_active"
    utilisateurActif = testLogin()
    return render_template('nouveauCompte.html',utilisateurActif = utilisateurActif,page1=page1,page2=page2,page3=page3,page4=page4)  
    
########################################################################################
#                               commande valider nouveau compte                        #
########################################################################################
@app.route('/validerNouveauCompte',methods=['POST','GET'])
def validerNouveauCompte():
    if request.method == 'POST':

        login = request.form['login']
        mdp = request.form['mdp']
        mdp2 = request.form['mdp2']

        utilisateurEnBase = user.query.filter_by(login = login).first()

        if utilisateurEnBase:
            flash("login non disponible")
            return redirect('/nouveauCompte')
        else:
            if mdp == mdp2:

                new_user = user(login=login,mdp = generate_password_hash(mdp))

                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash( "compte créé avec succes")
                    session['username'] = user.login
                    return redirect('/pagePrincipale')

                except:
                    flash( "probleme dans la création du compte")
                    return redirect('/nouveauCompte')
            else:
                flash( "les mots de passe ne correspondent pas")
                return redirect('/nouveauCompte')
    else:
        return redirect('/')

########################################################################################
#                               affichage page principale                              #
########################################################################################
@app.route('/pagePrincipale',methods=['POST','GET'])
def pagePrinc():
    page1 = "active"
    page2 = "non_active"
    page3 = "non_active"
    page4 = "non_active"
    if request.method == 'POST':

        liste_groupe_de = dice_group.query.filter(dice_group.owner == session['username']).all()
        return render_template('pagePrincipale.html',  liste_groupe_de=liste_groupe_de ,utilisateurActif = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
    else:
        if 'username' in session:

            liste_groupe_de = dice_group.query.filter(dice_group.owner == session['username']).all()
            return render_template('pagePrincipale.html',  liste_groupe_de=liste_groupe_de ,utilisateurActif = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
        else:
            return redirect('/')

########################################################################################
#                               affichage page création dé                             #
########################################################################################
@app.route('/creationDe',methods=['POST','GET'])
def creationDe():
    page1 = "non_active"
    page2 = "active"
    page3 = "non_active"
    page4 = "non_active"
    if request.method == 'POST':
        listeDe = dice.query.filter(dice.owner == session['username']).all()
        return render_template('creationDe.html', listeDe=listeDe ,utilisateurActif = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
    else:

        if 'username' in session:
            listeDe = dice.query.filter(dice.owner == session['username']).all()
            return render_template('creationDe.html', listeDe=listeDe  ,utilisateurActif = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
        else:
            return redirect('/')

########################################################################################
#                               commande valider dé                                    #
########################################################################################
@app.route('/valideDe',methods=['POST','GET'])
def validerDe():
    if request.method == 'POST':

        new_dice = dice(name=request.form['nomDuDe'],value = request.form['nbDeFace'])
        new_dice.owner = session['username']

        db.session.add(new_dice)
        db.session.commit()
        
        return redirect('/creationDe')
    else:
        if 'username' in session:
            return redirect('/creationDe')
        else:
            return redirect('/')

########################################################################################
#                               commande supprimer dé                                  #
########################################################################################
@app.route('/suprimerDe/<int:id>',methods=['POST','GET'])
def suprimeDe(id):
    dice_to_delete = dice.query.get_or_404(id)
    print(id)
    try:
        db.session.delete(dice_to_delete)
        db.session.commit()
        return redirect('/creationDe')
    except:
        flash("impossible de supprimer ce dé ,verifier qu'il n'appartient pas a un lancé")
        return redirect('/creationDe')


########################################################################################
#                               affichage page création de lancé                       #
########################################################################################
@app.route('/creationLance',methods=['POST','GET'])
def creationLance():
    page1 = "non_active"
    page2 = "non_active"
    page3 = "active"
    page4 = "non_active"
    if request.method == 'POST':
        listeLance = dice_group.query.filter(dice_group.owner == session['username']).all()
        return render_template('creationLance.html', listeLance=listeLance , utilisateurActif = session['username'],page1=page1,page2=page2,page3=page3,page4=page4) 
    else:
        if 'username' in session:
            listeLance = dice_group.query.filter(dice_group.owner == session['username']).all()
            return render_template('creationLance.html', listeLance=listeLance , utilisateurActif = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
        else:
            return redirect('/')

########################################################################################
#                               commande valider nouveau lancé                         #
########################################################################################
@app.route('/validerLance',methods=['POST','GET'])
def validerLance():
    if request.method == 'POST':

        print (request.form['nomDuLance'])
     
        new_dice_group = dice_group(name=request.form['nomDuLance'])
        new_dice_group.owner = session['username']
        new_dice_group.nb_de = 0
        
        db.session.add(new_dice_group)
        db.session.commit()
        
        return redirect('/creationLance')
    else:
        return redirect('/')

########################################################################################
#                               commande supprimer lancé                               #
########################################################################################
@app.route('/suprimerLance/<int:id>',methods=['POST','GET'])
def suprimeLance(id):
    dice_group_to_delete = dice_group.query.get_or_404(id)
    listeJonction = dice_list_group.query.filter(dice_list_group.idGroup == id).all()
    try:
        db.session.delete(dice_group_to_delete)
        for jonction in listeJonction:
            db.session.delete(jonction)
        db.session.commit()
        return redirect('/creationLance')
    except:
        flash("problème rencontré pendnat la tentative de suppression")
        return redirect('/creationLance')

########################################################################################
#                               affichage page parametrage de lancé                    #
########################################################################################
@app.route('/parametrerLance/<int:id>',methods=['POST','GET'])
def parametrerLance(id):
    if request.method == 'POST':
        groupeSelectionne = dice_group.query.get_or_404(id)
        session['idGroupeSelectionne'] = id
        
        listeDe = dice.query.filter(dice.owner == session['username']).all()
        
        listeJonction = dice_list_group.query.filter(dice_list_group.idGroup == groupeSelectionne.id).all()
        
        return render_template('parametrageLance.html', listeDe=listeDe , listeJonction=listeJonction , utilisateurActif = session['username'] , groupeSelectionne = groupeSelectionne)
    else:
        return redirect('/')

########################################################################################
#                               commande ajouter un dé au lancé                        #
########################################################################################
@app.route('/ajouterAuLance/<int:id>',methods=['POST','GET'])
def ajouterDe(id):
    if request.method == 'POST':
        dice_to_add = dice.query.get_or_404(id)
        group_to_add_dice = dice_group.query.get_or_404(session['idGroupeSelectionne'])

        new_dice_list_group = dice_list_group( idDice=dice_to_add.id , idGroup=group_to_add_dice.id )
        db.session.add(new_dice_list_group)
    
        nb_de_de_dans_jonction = dice_list_group.query.filter(dice_list_group.idGroup == group_to_add_dice.id).count()
        group_to_add_dice.nb_de = nb_de_de_dans_jonction
        db.session.commit()
        
        print(new_dice_list_group)

        return redirect(url_for('parametrerLance', id=session['idGroupeSelectionne']),code=307)
    else:
        return redirect('/')

########################################################################################
#                               commande enlever un dé au lancé                        #
########################################################################################
@app.route('/enleverAuLance/<int:id>',methods=['POST','GET'])
def enleverDe(id):
    if request.method == 'POST':
        # dice_to_remove = dice.query.get_or_404(id)
        group_to_remove_dice = dice_group.query.get_or_404(session['idGroupeSelectionne'])

        dice_list_group_to_remove = dice_list_group.query.get_or_404(id)
        db.session.delete(dice_list_group_to_remove)

        nb_de_de_dans_jonction = dice_list_group.query.filter(dice_list_group.idGroup == group_to_remove_dice.id).count()
        group_to_remove_dice.nb_de = nb_de_de_dans_jonction
        db.session.commit()
        
        return redirect(url_for('parametrerLance', id=session['idGroupeSelectionne']),code=307)
    else:
        return redirect('/')

########################################################################################
#                               commande lancer un groupe de dé                        #
########################################################################################
@app.route('/lancerGroupe/<int:id>',methods=['POST','GET'])
def lancerGroup(id):
    if request.method == 'POST':
        # declaration et initialisation de la variable resultat du lancé
        resultatLance = 0
        # recuperation du groupe sur lequel effectuer le lancé
        dice_group_to_launch = dice_group.query.get_or_404(id)
        # list des jonction du groupe selectionné
        listeJonction = dice_list_group.query.filter(dice_list_group.idGroup == dice_group_to_launch.id).all()
    
        new_historique_lance = historique_lance(lance_id = id)
        db.session.add(new_historique_lance)


        for jonction in listeJonction:
            print (jonction.id)
            deSelect = dice.query.filter(dice.id == jonction.idDice).first()
            print (deSelect.name)
            result = random.randint (1,deSelect.value)
            dice_result = result
            resultatLance += dice_result
            print('resultat individuel ' + str(dice_result))
            jonction.last_result = dice_result

            new_historique = historique( value = result , historiqueLance_id = new_historique_lance.id , de_id = deSelect.id)
            db.session.add(new_historique)

            
        
        print('resultat total ' + str(resultatLance))
        dice_group_to_launch.last_result = resultatLance

        new_historique_lance.valeur_total = resultatLance
        print('id du historiquelance')
        print(new_historique_lance.id)
        db.session.commit()

        return redirect('/pagePrincipale')
    else:
        return redirect('/')




########################################################################################
#                               affichage page historique du groupe                    #
########################################################################################
@app.route('/historique/<int:id>',methods=['POST','GET'])
def historiqueAff(id):
    if request.method == 'POST':
        
        nom_lance = dice_group.query.filter(dice_group.id == id).first().name

        # on recupere la liste des historiques liés a ce lancé
        listeHist = historique_lance.query.filter(historique_lance.lance_id == id).all()
        # on initialise un liste vide d'historique a afficher
        liste_hist_aff = []
       
        # pour chaque éléments dans la liste d'historique on crée un objet pour l'affichage  
        for hist in listeHist:
            hist_aff = historique_affichage()

            hist_aff.numero_lance = hist.id
            hist_aff.total = 0
            hist_aff.total_max =0
            hist_aff.liste_detail= []
            hist_aff.date_created = 'date : '+str(hist.date_created.date())\
                                    +' heure : '+str(hist.date_created.hour)\
                                    +':'+str(hist.date_created.minute)\
                                    +':'+str(hist.date_created.second)

            # liste des historique de dé lié a cet historique lancé
            liste_hist_de = historique.query.filter(historique.historiqueLance_id == hist.id).all()
            # pour chaque éléments historique dé on crée un objet detail_de que l'on ajoute a la liste de detail
            for hist_de in liste_hist_de:

                detail = detail_de()

                detail.nom = dice.query.filter(dice.id == hist_de.de_id).first().name
                detail.face = dice.query.filter(dice.id == hist_de.de_id).first().value
                detail.value = hist_de.value

                hist_aff.total += detail.value
                hist_aff.total_max += detail.face
                hist_aff.liste_detail.append(detail)
                 
            liste_hist_aff.append(hist_aff)
  
        return render_template('historique.html', liste_hist_aff=liste_hist_aff , utilisateurActif = session['username'] ,id=id,nom_lance=nom_lance)
    else:
        return redirect('/')
      
 
########################################################################################
#                               commande supprimer l'historique d'un groupe de dé      #
########################################################################################
@app.route('/suprimerHistoriqueDe/<int:id>',methods=['POST','GET'])
def supprimerHistoriqueDe(id):
    if request.method == 'POST':
        
        listHistoriqueLanceToDelete = historique_lance.query.filter(historique_lance.lance_id == id).all()

        for histLance in listHistoriqueLanceToDelete:

            listeHist = historique.query.filter(historique.historiqueLance_id == histLance.id).all()

            for hist in listeHist:

                db.session.delete(hist)

            db.session.delete(histLance)
    
        db.session.commit()

        return redirect(url_for('historiqueAff', id=id),code=307)
    else:
        return redirect('/')
      
         