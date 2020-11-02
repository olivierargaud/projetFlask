# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app











# class User:
#     def __init__(self, id, username, password):
#         self.id = id
#         self.username = username
#         self.password = password
    
#     def __repr__(self):
#         return f'<User : {self.username}>'
    
# users = []
# users.append(User(id=1, username='Mathis', password='password'))
# users.append(User(id=2, username='Olivier', password='secret'))

# def create_app():
#     app = Flask(__name__)
#     app.secret_key = 'motdepasse'

#     @app.before_request
#     def before_request():
#         if 'user_id' in session:
#             user = [x for x in users if x.id == session['user_id']][0]
#             g.user = user


#     @app.route('/')
#     def homepage():
#         return render_template('homepage.html')

#     @app.route('/historique/')
#     def historique():
#         return render_template('historique.html')

#     @app.route("/login/", methods=["POST", "GET"])
#     def login():
#         if request.method == "POST":
#             session.pop('user_id', None)
#             username = request.form['username']
#             password = request.form['password']
            
#             user = [x for x in users if x.username == username][0]
#             if user and user.password == password:
#                 session['user_id'] = user.id
#                 return redirect(url_for('profile'))

#             return redirect(url_for('login'))

#         return render_template("login.html")


#     @app.route("/profile/")
#     def profile():
#         if not g.user:
#             return redirect(url_for('login'))
#         return render_template("profile.html")

#     @app.route("/<usr>/")
#     def user(usr):
#         return f"<h1>{usr}</h1>"

#     return app