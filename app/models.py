from app import db
from flask_login import UserMixin

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    location = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    assets = db.relationship('Asset', backref='owner', lazy='dynamic')
