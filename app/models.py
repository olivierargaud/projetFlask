from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Des(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NbrDeFace = db.Column(db.Integer)
    Proprietaire = db.Column(db.String(100))
    NomProprietaire = db.Column(db.String(100))
    NomDuDes = db.Column(db.String(100))
    LastResult = db.Column(db.Integer, nullable=False)