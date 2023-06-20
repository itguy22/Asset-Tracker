from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# This is the association table for the many-to-many relationship between User and Company.
user_companies = db.Table('user_companies',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('company_id', db.Integer, db.ForeignKey('company.id'))
)

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    location = db.Column(db.String(64))
    ip_address= db.Column(db.String(64))
    serial_number = db.Column(db.String(64))
    service_tag = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))  # Assets belong to Companies

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    companies = db.relationship('Company', secondary=user_companies, backref=db.backref('users', lazy='dynamic'))  # Users can have multiple Companies
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    assets = db.relationship('Asset', backref='company', lazy='dynamic')  # A Company can have multiple Assets
    address = db.Column(db.String(128))
    phone = db.Column(db.String(64))

