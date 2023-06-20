from flask import request
from flask_login import login_required
from app import db, bcrypt, login as login_manager
from app.models import User, Company
from app.forms import RegistrationForm, LoginForm
from flask import render_template, url_for, flash, redirect
from flask_login import login_user, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def configure_routes(app):

    @app.route('/')
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        else:
            return redirect(url_for('register'))
        
    @app.route("/register", methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('home'))
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data) # corrected line
            user.set_password(form.password.data) # add this line
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
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)
    
    @app.route('/home')
    def home():
        companies = Company.query.all()  # fetch all companies
        return render_template('index.html', companies=companies)





@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
