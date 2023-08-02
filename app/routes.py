from flask import request
from flask_login import login_required
from app import db, bcrypt, login as login_manager
from app.models import User, Company, Asset
from app.forms import RegistrationForm, LoginForm, AssetForm, CompanyForm, EditCompanyForm, DeleteCompanyForm
from flask import render_template, url_for, flash, redirect, abort
from flask_login import login_user, current_user, logout_user
from flask import current_app as app
from sqlalchemy import or_

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def configure_routes(app):

    @app.route("/dashboard")
    @login_required
    def dashboard():
        companies = current_user.companies # Get the companies associated with the current user
        return render_template('index.html', title='Dashboard', companies=companies)


    @app.route("/")
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('dashboard'))  # Redirect to the authenticated user's page
        return render_template('home.html')  # Show the home page to unauthenticated users



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
            if user:
                print(f"Found user: {user.username}")
                if user.check_password(form.password.data):
                    print("Password match.")
                    login_user(user, remember=form.remember.data)
                    print("User should be logged in and redirected.")
                    return redirect(url_for('home'))
                else:
                    print("Password does not match.")
            else:
                print("No user found.")
            flash('Login Unsuccessful. Please check username and password', 'danger')
        return render_template('login.html', title='Login', form=form)
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('login'))


        
    @app.route("/new_company", methods=['GET', 'POST'])
    @login_required
    def new_company():
        form = CompanyForm()  # Assumes you have a CompanyForm defined in forms.py
        if form.validate_on_submit():
            for company in current_user.companies:
                if company.name == form.name.data:
                    flash('You already have a company with this name.', 'danger')
                    return redirect(url_for('new_company'))
                    break  # breaks the loop as soon as a match is found
            new_company = Company(name=form.name.data, address=form.address.data, phone=form.phone.data)
            new_company.users.append(current_user)
            db.session.add(new_company)
            db.session.commit()

            flash('New company has been created!', 'success')
            return redirect(url_for('home'))  # or redirect to any page you like
        return render_template('new_company.html', title='New Company', form=form)


    @app.route("/new_asset", methods=['GET', 'POST'])
    @login_required
    def new_asset():
        form = AssetForm()
        if form.validate_on_submit():
            app.logger.info('Form validated successfully.')
            new_asset = Asset(name=form.name.data, description=form.description.data, location=form.location.data, ip_address=form.ip_address.data, serial_number=form.serial_number.data, service_tag=form.service_tag.data, company_id=form.company_id.data)  # Assuming your AssetForm includes a company_id field
            db.session.add(new_asset)
            db.session.commit()
            flash('New asset has been added!', 'success')
            return redirect(url_for('home'))  # or redirect to any page you like
        return render_template('new_asset.html', title='New Asset', form=form)
    
    @app.route('/edit_company/<int:company_id>', methods=['GET', 'POST'])
    @login_required
    def edit_company(company_id):
        company = Company.query.get_or_404(company_id)
        print(company.__dict__)  # For debugging purposes.

        if company not in current_user.companies:
            abort(403)

        form = EditCompanyForm()

        # For debugging purposes. Print the form data before and after assigning the company data to it.
        print(f'Form data before assignment: Name - {form.name.data}, Address - {form.address.data}, Phone - {form.phone.data}')
        
        if request.method == 'GET':
            form.name.data = company.name
            form.address.data = company.address
            form.phone.data = company.phone

        print(f'Form data after assignment: Name - {form.name.data}, Address - {form.address.data}, Phone - {form.phone.data}')
        # End of debugging block.

        delete_form = DeleteCompanyForm()

        if form.validate_on_submit():
            company.name = form.name.data
            company.address = form.address.data
            company.phone = form.phone.data
            db.session.commit()
            flash('Your changes have been saved.')
            return redirect(url_for('home'))
    
        if delete_form.validate_on_submit():
            db.session.delete(company)
            db.session.commit()
            flash('The company has been deleted.')
            return redirect(url_for('home'))

        return render_template('edit_company.html', title='Edit Company',
                                form=form, delete_form=delete_form, company=company)


    @app.route('/company/<int:company_id>/assets', methods=['GET', 'POST'])
    @login_required
    def assets(company_id):
        # Log the incoming company ID
        app.logger.info('Accessing assets for company with id %s', company_id)

        # Fetch the company and its associated assets from the database
        company = Company.query.get_or_404(company_id)

        # Log details about the company
        app.logger.debug('Found company: %s', company.name)

        if current_user not in company.users:
            app.logger.warning('User %s tried to access company %s without permission', current_user.id, company_id)
            abort(403)  # If the user doesn't have access to this company, return a 403 error

        assets = Asset.query.filter_by(company_id=company.id).all()

        # Log the number of assets found
        app.logger.debug('Found %s assets', len(assets))

        form = AssetForm()
        if form.validate_on_submit():
            new_asset = Asset(
                name=form.name.data,
                ip_address=form.ip_address.data,
                serial_number=form.serial_number.data,
                service_tag=form.service_tag.data,
                location=form.location.data,
                company_id=company.id
            )
            db.session.add(new_asset)
            db.session.commit()
            flash('New asset has been added!', 'success')
            return redirect(url_for('assets', company_id=company.id)) 

        return render_template('assets.html', title='Assets', form=form, assets=assets, company=company)


    @app.route('/company/<int:company_id>/asset/<int:asset_id>/update', methods=['GET', 'POST'])
    @login_required
    def update_asset(company_id, asset_id):
        # Update asset logic here
        # Fetch the asset and check if the user has permission to update it
        asset = Asset.query.get_or_404(asset_id)
        if asset.company_id != company_id:
            abort(403)  # If the asset doesn't belong to the company, return a 403 error

        form = AssetForm()
        if form.validate_on_submit():
            asset.name = form.name.data
            asset.ip_address = form.ip_address.data
            asset.serial_number = form.serial_number.data
            asset.service_tag = form.service_tag.data
            asset.location = form.location.data
            db.session.commit()
            flash('Asset has been updated!', 'success')
            return redirect(url_for('assets', company_id=company_id))

        elif request.method == 'GET':
            form.name.data = asset.name
            form.ip_address.data = asset.ip_address
            form.serial_number.data = asset.serial_number
            form.service_tag.data = asset.service_tag
            form.location.data = asset.location
        return render_template('update_asset.html', title='Update Asset', form=form, company_id=company_id, asset_id=asset_id)

    @app.route('/company/<int:company_id>/asset/<int:asset_id>/delete', methods=['POST'])
    @login_required
    def delete_asset(company_id, asset_id):
        # Delete asset logic here
        asset = Asset.query.get_or_404(asset_id)
        if asset.company_id != company_id:
            abort(403)  # If the asset doesn't belong to the company, return a 403 error

        db.session.delete(asset)
        db.session.commit()
        flash('Asset has been deleted!', 'success')
        return redirect(url_for('assets', company_id=company_id))






