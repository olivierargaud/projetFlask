from flask import Flask,render_template, request, redirect
app = Flask(__name__)

@app.route('/')
def loginDeBase():
     return render_template('login.html')

@app.route('/',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        return render_template('login.html')  
    else:
        return redirect('/')

@app.route('/nouveauCompte')
def nouveauCompteDeBase():
    return render_template('nouveauCompte.html')

@app.route('/nouveauCompte',methods=['POST','GET'])
def nouveauCompte():
    if request.method == 'POST':
        return render_template('nouveauCompte.html')  
    else:
        return redirect('/')