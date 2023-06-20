from flask import request
from flask_login import login_required
from app import db, bcrypt, login as login_manager
from app.models import User, Company
from app.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user
from sqlalchemy import or_

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def configure_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')


    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            existing_user = User.query.filter((User.email == form.email.data) | (User.username == form.username.data)).first()
            if existing_user:
                flash('A user with this email or username already exists. Please use a different email or username.', 'danger')
                return redirect(url_for('register'))
            user = User(username=form.username.data, email=form.email.data) 
            user.set_password(form.password.data) 
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        return render_template('register.html', title='Register', form=form)


    @app.route("/login", methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                print("User should be logged in and redirected.")
                return redirect(url_for('home'))
        else:
            print("User could not be logged in.")
            flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)

    
    @app.route('/home')
    def home():
        if current_user.is_authenticated:
            companies = Company.query.all()  # fetch all companies
            return render_template('index.html', companies=companies)
        else:
            return redirect(url_for('login'))  # redirect to 'login' if the user is not authenticated

