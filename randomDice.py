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
    dice_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    value = db.Column(db.Integer, nullable = False)
    owner = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    group = db.relationship('junction_dice_group', backref=db.backref('dice', lazy='joined'))
    group = db.relationship('dice_historic', backref=db.backref('dice', lazy='joined'))
    
    def __repr__(self):
        return '<Dice %r , %r faces>' % (self.name , self.value)

########################################################################################
#                                                                                      #
########################################################################################
class dice_group(db.Model):
    group_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    owner = db.Column(db.String(50), nullable = False)
    last_result = db.Column(db.Integer)
    dice_count = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return '<Dice Group %r , %r dice>' % (self.name,self.nb_de)

########################################################################################
#                                                                                      #
########################################################################################
class junction_dice_group(db.Model):
    junction_dice_group_id = db.Column(db.Integer, primary_key = True)
    dice_id = db.Column(db.Integer, ForeignKey('dice.dice_id'), nullable = False)
    group_id = db.Column(db.Integer, ForeignKey('dice_group.group_id'), nullable = False)
    
    def __repr__(self):
        return '<Dice %r Group %r>' % (self.dice_id , self.group_id)

########################################################################################
#                                                                                      #
########################################################################################
class user(db.Model):
    login = db.Column(db.String(200), nullable = False , primary_key = True)
    password = db.Column(db.String(200), nullable = False)
    
    def __repr__(self):
        return '<User %r >' % self.password 

########################################################################################
#                                                                                      #
########################################################################################
class roll_historic(db.Model):
    roll_historic_id = db.Column(db.Integer, primary_key = True)
    dice_group_id = db.Column(db.Integer, ForeignKey('dice_group.group_id'), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<historic roll nb %r >' % self.roll_historic_id 

########################################################################################
#                                                                                      #
########################################################################################
class dice_historic(db.Model):
    dice_historic_id = db.Column(db.Integer, primary_key = True)
    value = db.Column(db.Integer)
    dice_id = db.Column(db.Integer, ForeignKey('dice.dice_id'), nullable = False)
    roll_historic_id = db.Column(db.Integer, ForeignKey('roll_historic.roll_historic_id'), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self):
        return '<historice dice nb %r >' % self.dice_historic_id 



######################################################################################################################################################
#                                                                                                                                                    #
######################################################################################################################################################


########################################################################################
#                                                                                      #
########################################################################################
class historic_to_show():
    roll_nb = 0
    total_max = 0
    total = 0
    date_created = ''
    detail_list = []

    def __repr__(self):
        return '<Historic number %r , %r / %r >' % (self.roll_nb , self.total , self.total_max) 

########################################################################################
#                                                                                      #
########################################################################################
class dice_detail():
    name = ''
    face = 0
    value = 0
    
    def __repr__(self):
        return '<Histori dice %r , %r / %r >' % (self.name , self.value , self.face) 


######################################################################################################################################################
#                                                           function                                                                                 #
######################################################################################################################################################

########################################################################################
#                                                                                      #
########################################################################################
def testLogin():
    if 'username' in session:
        user_logged = session['username']
    else:
        user_logged = "none"
    return user_logged



######################################################################################################################################################
#                                                           route                                                                                    #
######################################################################################################################################################

########################################################################################
#                               root                                                   #
########################################################################################
@app.route('/',methods=['POST','GET'])
def login():
    page1 = "non_active"
    page2 = "non_active"
    page3 = "non_active"
    page4 = "active"
    user_logged = testLogin()
    return render_template('login.html',user_logged = user_logged,page1=page1,page2=page2,page3=page3,page4=page4)  
   
########################################################################################
#                                login                                                 #
########################################################################################
@app.route('/login',methods=['POST','GET'])
def validerLogin():
    if request.method == 'POST':
        username = request.form['login']
        password = request.form['password1']

        user_in_database = user.query.filter_by(login = username).first()

        if user_in_database:
            if check_password_hash(user_in_database.password, password):
                session['username'] = username
                return redirect('/pagePrincipale')
            else:
                flash("mauvais mot de passe")
                return redirect('/')
        else:
            flash("utilisateur inconnu , veuillez créer un nouveau compte")
            return redirect('/')
    else:
        return redirect('/')

########################################################################################
#                                logout                                                #
########################################################################################
@app.route('/logout',methods=['POST','GET'])
def logout():
        session.pop('username', None)
        return redirect('/')
  

########################################################################################
#                               nouveauCompte page                                     #
########################################################################################
@app.route('/nouveauCompte',methods=['POST','GET'])
def nouveauCompte():
    page1 = "non_active"
    page2 = "non_active"
    page3 = "non_active"
    page4 = "non_active"
    user_logged = testLogin()
    return render_template('nouveauCompte.html',user_logged = user_logged,page1=page1,page2=page2,page3=page3,page4=page4)  
    
########################################################################################
#                               submit new account                                     #
########################################################################################
@app.route('/submitNewAccount',methods=['POST','GET'])
def submitNewAccount():
    if request.method == 'POST':

        login = request.form['login']
        password = request.form['password']
        password2 = request.form['password2']

        user_in_database = user.query.filter_by(login = login).first()

        if user_in_database:
            flash("login non disponible")
            return redirect('/nouveauCompte')
        else:
            if password == password2:

                new_user = user(login=login,password = generate_password_hash(password))

                try:
                    db.session.add(new_user)
                    db.session.commit()
                    flash( "compte créé avec succes")
                    session['username'] = new_user.login
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
#                               page principale                                        #
########################################################################################
@app.route('/pagePrincipale',methods=['POST','GET'])
def pagePrinc():
    page1 = "active"
    page2 = "non_active"
    page3 = "non_active"
    page4 = "non_active"
    if request.method == 'POST':

        dice_group_list = dice_group.query.filter(dice_group.owner == session['username']).all()
        return render_template('pagePrincipale.html',  dice_group_list=dice_group_list ,user_logged = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
    else:
        if 'username' in session:

            dice_group_list = dice_group.query.filter(dice_group.owner == session['username']).all()
            return render_template('pagePrincipale.html',  dice_group_list=dice_group_list ,user_logged = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
        else:
            return redirect('/')

########################################################################################
#                                 "création dé" page                                   #
########################################################################################
@app.route('/creationDe',methods=['POST','GET'])
def creationDe():
    page1 = "non_active"
    page2 = "active"
    page3 = "non_active"
    page4 = "non_active"
    if request.method == 'POST':
        dice_list = dice.query.filter(dice.owner == session['username']).all()
        return render_template('creationDe.html', dice_list=dice_list ,user_logged = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
    else:

        if 'username' in session:
            dice_list = dice.query.filter(dice.owner == session['username']).all()
            return render_template('creationDe.html', dice_list=dice_list  ,user_logged = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
        else:
            return redirect('/')

########################################################################################
#                               create dice                                            #
########################################################################################
@app.route('/createDice',methods=['POST','GET'])
def createDice():
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
#                               delete dice                                            #
########################################################################################
@app.route('/deleteDice/<int:id>',methods=['POST','GET'])
def deleteDice(id):
    dice_to_delete = dice.query.get_or_404(id)

    try:
        db.session.delete(dice_to_delete)
        db.session.commit()
        return redirect('/creationDe')
    except:
        flash("impossible de supprimer ce dé ,verifier qu'il n'appartient pas a un lancé ou a un historique")
        return redirect('/creationDe')


########################################################################################
#                               "création de lancé" page                               #
########################################################################################
@app.route('/creationLance',methods=['POST','GET'])
def creationLance():
    page1 = "non_active"
    page2 = "non_active"
    page3 = "active"
    page4 = "non_active"
    if request.method == 'POST':
        group_list = dice_group.query.filter(dice_group.owner == session['username']).all()
        return render_template('creationLance.html', group_list=group_list , user_logged = session['username'],page1=page1,page2=page2,page3=page3,page4=page4) 
    else:
        if 'username' in session:
            group_list = dice_group.query.filter(dice_group.owner == session['username']).all()
            return render_template('creationLance.html', group_list=group_list , user_logged = session['username'],page1=page1,page2=page2,page3=page3,page4=page4)
        else:
            return redirect('/')

########################################################################################
#                               create dice group                                      #
########################################################################################
@app.route('/createGroup',methods=['POST','GET'])
def createGroup():
    if request.method == 'POST':

        new_dice_group = dice_group(name=request.form['nomDuLance'])
        new_dice_group.owner = session['username']
        new_dice_group.nb_de = 0
        
        db.session.add(new_dice_group)
        db.session.commit()
        
        return redirect('/creationLance')
    else:
        return redirect('/')

########################################################################################
#                               delete dice group                                      #
########################################################################################
@app.route('/deleteGroup/<int:id>',methods=['POST','GET'])
def deleteGroup(id):
    dice_group_to_delete = dice_group.query.get_or_404(id)
    junction_list = junction_dice_group.query.filter(junction_dice_group.group_id == id).all()
    try:
        db.session.delete(dice_group_to_delete)
        for junction in junction_list:
            db.session.delete(junction)
        db.session.commit()
        return redirect('/creationLance')
    except:
        flash("problème rencontré pendnat la tentative de suppression")
        return redirect('/creationLance')

########################################################################################
#                               "parametrage de lancé" page                            #
########################################################################################
@app.route('/parametrerLance/<int:id>',methods=['POST','GET'])
def parametrerLance(id):
    if request.method == 'POST':
        group_selected = dice_group.query.get_or_404(id)
        session['group_selected_id'] = id
        
        dice_list = dice.query.filter(dice.owner == session['username']).all()
        
        junction_list = junction_dice_group.query.filter(junction_dice_group.group_id == group_selected.group_id).all()
        
        return render_template('parametrageLance.html', dice_list=dice_list , junction_list=junction_list , user_logged = session['username'] , group_selected = group_selected)
    else:
        return redirect('/')

########################################################################################
#                               add dice to group                                      #
########################################################################################
@app.route('/addDiceToGroup/<int:id>',methods=['POST','GET'])
def addDiceToGroup(id):
    if request.method == 'POST':
        dice_to_add = dice.query.get_or_404(id)
        group_to_add_dice = dice_group.query.get_or_404(session['group_selected_id'])

        new_junction_dice_group = junction_dice_group( dice_id=dice_to_add.dice_id , group_id=group_to_add_dice.group_id )
        db.session.add(new_junction_dice_group)
    
        group_to_add_dice.dice_count = junction_dice_group.query.filter(junction_dice_group.group_id == group_to_add_dice.group_id).count()
        db.session.commit()
        
    
        return redirect(url_for('parametrerLance', id=session['group_selected_id']),code=307)
    else:
        return redirect('/')

########################################################################################
#                               remove dice to group                                   #
########################################################################################
@app.route('/removeDiceToGroup/<int:id>',methods=['POST','GET'])
def removeDiceToGroup(id):
    if request.method == 'POST':
        group_to_remove_dice = dice_group.query.get_or_404(session['group_selected_id'])

        junction_dice_group_to_remove = junction_dice_group.query.get_or_404(id)
        db.session.delete(junction_dice_group_to_remove)
 
        group_to_remove_dice.dice_count = junction_dice_group.query.filter(junction_dice_group.group_id == group_to_remove_dice.group_id).count()
        db.session.commit()
        
        return redirect(url_for('parametrerLance', id=session['group_selected_id']),code=307)
    else:
        return redirect('/')

########################################################################################
#                               group launch                                           #
########################################################################################
@app.route('/groupLaunch/<int:id>',methods=['POST','GET'])
def groupLaunch(id):
    if request.method == 'POST':

        total_result = 0
        dice_group_to_launch = dice_group.query.get_or_404(id)
        junction_list = junction_dice_group.query.filter(junction_dice_group.group_id == dice_group_to_launch.group_id).all()
    
        new_roll_historic = roll_historic(dice_group_id = id)
        db.session.add(new_roll_historic)

        if len(junction_list) == 0:
            flash('pas de dé dans ce groupe, veuillez parametrer ce groupe')
            return redirect('/pagePrincipale')
        else:    
            for junction in junction_list:
                deSelect = dice.query.filter(dice.dice_id == junction.dice_id).first()
                result = random.randint (1,deSelect.value)
                dice_result = result
                total_result += dice_result
                junction.last_result = dice_result

                new_dice_historic = dice_historic( value = result , roll_historic_id = new_roll_historic.roll_historic_id , dice_id = deSelect.dice_id)
                db.session.add(new_dice_historic)
            
            dice_group_to_launch.last_result = total_result
            new_roll_historic.valeur_total = total_result
            db.session.commit()

            return redirect('/pagePrincipale')
    else:
        return redirect('/')




########################################################################################
#                               "historique du groupe" page                            #
########################################################################################
@app.route('/historique/<int:id>',methods=['POST','GET'])
def historique(id):
    if request.method == 'POST':
        
        selected_dice_group_name = dice_group.query.filter(dice_group.group_id == id).first().name

        roll_historic_list = roll_historic.query.filter(roll_historic.dice_group_id == id).all()
        
        roll_historic_list_to_show = []
       
        for hist in roll_historic_list:
            hist_to_show = historic_to_show()

            hist_to_show.numero_lance = hist.roll_historic_id
            hist_to_show.total = 0
            hist_to_show.total_max =0
            hist_to_show.detail_list= []
          
            hist_to_show.date_created = str(hist.date_created.strftime("%H:%M:%S"))+'  '
            hist_to_show.date_created += str(hist.date_created.strftime("%d/%m/%Y"))
           


            dice_historic_list = dice_historic.query.filter(dice_historic.roll_historic_id == hist.roll_historic_id).all()
            
            for dice_hist in dice_historic_list:

                new_dice_detail = dice_detail()

                new_dice_detail.name = dice.query.filter(dice.dice_id == dice_hist.dice_id).first().name
                new_dice_detail.face = dice.query.filter(dice.dice_id == dice_hist.dice_id).first().value
                new_dice_detail.value = dice_hist.value

                hist_to_show.total += new_dice_detail.value
                hist_to_show.total_max += new_dice_detail.face
                hist_to_show.detail_list.append(new_dice_detail)
                 
            roll_historic_list_to_show.append(hist_to_show)
  
        return render_template('historique.html', roll_historic_list_to_show=roll_historic_list_to_show , user_logged = session['username'] ,id=id,selected_dice_group_name=selected_dice_group_name)
    else:
        return redirect('/')
      
 
########################################################################################
#                               delete historic                                        #
########################################################################################
@app.route('/deleteHistoric/<int:id>',methods=['POST','GET'])
def deleteHistoric(id):
    if request.method == 'POST':
        
        roll_hitoric_to_delete_list = roll_historic.query.filter(roll_historic.dice_group_id == id).all()

        for roll_hist_to_delete in roll_hitoric_to_delete_list:

            dice_hist_list = dice_historic.query.filter(dice_historic.roll_historic_id == roll_hist_to_delete.roll_historic_id).all()

            for hist in dice_hist_list:

                db.session.delete(hist)

            db.session.delete(roll_hist_to_delete)
    
        dice_group_to_reset = dice_group.query.get_or_404(id)
        dice_group_to_reset.last_result = None

        db.session.commit()

        return redirect('/pagePrincipale')
    else:
        return redirect('/')
      
         