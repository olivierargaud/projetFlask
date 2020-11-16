from flask_login import UserMixin
from . import db

## Database table declaration ##

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Des(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NumberOfFaces = db.Column(db.Integer)
    Owner = db.Column(db.String(100))
    OwnerName = db.Column(db.String(100))
    DiceName = db.Column(db.String(100))
    LastResult = db.Column(db.Integer, nullable=False)