from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_login import UserMixin
import os
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask import render_template, flash, redirect, url_for
from flask_login import login_required, current_user

load_dotenv


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class AssetForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description')
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    location = db.Column(db.String(64))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128))
    password = db.Column(db.String(64))
    assets = db.relationship('Asset', backref='owner', lazy='dynamic')


"""@app.route('/')
def home():
    return 'Hello, World!'"""

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = AssetForm()
    if form.validate_on_submit():
        asset = Asset(name=form.name.data, description=form.description.data, owner=current_user)
        db.session.add(asset)
        db.session.commit()
        flash('Your asset has been added.')
        return redirect(url_for('index'))
    assets = current_user.assets.order_by(Asset.name.desc())
    return render_template('index.html', form=form, assets=assets)

@app.route('/asset/<id>', methods=['GET', 'POST'])
@login_required
def asset(id):
    asset = Asset.query.get_or_404(id)
    if asset.owner != current_user:
        abort(403)
    form = AssetForm(obj=asset)
    if form.validate_on_submit():
        asset.name = form.name.data
        asset.description = form.description.data
        db.session.commit()
        flash('Your asset has been updated.')
        return redirect(url_for('index'))
    return render_template('asset.html', form=form)

@app.route('/delete/<id>', methods=['POST'])
@login_required
def delete(id):
    form = DeleteForm()
    if form.validate_on_submit():
        asset = Asset.query.get_or_404(id)
        if asset.owner != current_user:
            abort(403)
        db.session.delete(asset)
        db.session.commit()
        flash('Your asset has been deleted.')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
