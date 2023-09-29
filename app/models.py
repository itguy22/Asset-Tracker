from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.schema import CheckConstraint

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
    
    # Asset type field
    asset_type = db.Column(db.String(50))  # Consider using db.Enum for stricter type checking
    
    # Common fields
    ip_address = db.Column(db.String(64))
    serial_number = db.Column(db.String(64))
    service_tag = db.Column(db.String(64))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    
    # Server-specific fields
    server_ip_address = db.Column(db.String(64), nullable=True)
    
    # PC-specific fields
    pc_ram = db.Column(db.Integer, nullable=True)
    pc_processor = db.Column(db.String(255), nullable=True)
    
    # Phone-specific fields
    phone_number = db.Column(db.String(15), nullable=True)
    mac_address = db.Column(db.String(15), nullable=True)
    
    # Switch-specific fields
    switch_ports = db.Column(db.Integer, nullable=True)
    switch_poe = db.Column(db.Boolean, nullable=True)
    
    # Database-level validation
    __table_args__ = (
        CheckConstraint(
            "(asset_type = 'Server' AND server_ip_address IS NOT NULL) OR "
            "(asset_type = 'PC' AND pc_ram IS NOT NULL AND pc_processor IS NOT NULL) OR "
            "(asset_type = 'Phone' AND phone_number IS NOT NULL) OR "
            "(asset_type = 'Switch' AND switch_ports IS NOT NULL AND switch_poe IS NOT NULL)", 
            name='valid_asset_data'
        ),
    )

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
    name = db.Column(db.String(64))  # remove the unique=True constraint
    assets = db.relationship('Asset', backref='company', lazy='dynamic')  # A Company can have multiple Assets
    address = db.Column(db.String(128))
    phone = db.Column(db.String(64))
