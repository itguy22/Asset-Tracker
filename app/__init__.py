from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv
from flask_bcrypt import Bcrypt
import os


load_dotenv()

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ.get('CSRF_SECRET_KEY')
uri = os.environ.get('DATABASE_URL')
if uri and uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'  # The login route

from app import routes, models
routes.configure_routes(app)  # Call the function here
print(app.config)