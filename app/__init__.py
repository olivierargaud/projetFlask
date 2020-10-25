# app/__init__.py

from flask import (
    Flask, redirect, render_template, url_for, request
)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
    
    def __repr__(self):
        return f'<User : {self.username}>'
    
users = []
users.append(User(id=1, username='Mathis', password='password'))
users.append(User(id=1, username='Olivier', password='secret'))

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def homepage():
        return render_template('homepage.html')

    @app.route('/historique/')
    def historique():
        return render_template('historique.html')

    @app.route("/login/", methods=["POST", "GET"])
    def login():
        return render_template("login.html")


    @app.route("/profile/")
    def profil():
        return render_template("profile.html")

    @app.route("/<usr>/")
    def user(usr):
        return f"<h1>{usr}</h1>"

    return app