from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_talisman import Talisman

app = Flask(__name__)
app.config['SECRET_KEY'] = '45cf93c4d41348cd9980674ade9a7356'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'danger'
bcrypt = Bcrypt(app)

# Defina suas políticas de segurança CSP
csp = {
    'default-src': ["'self'"],
    'script-src': ["'self'"],
    'style-src': ["'self'"],
    'img-src': ["'self'"],
    'connect-src': ["'self'"],
    'font-src': ["'self'"],
    'frame-src': ["'self'"],
}

# Configure o Flask-Talisman com a política CSP
Talisman(app, content_security_policy=csp)

# Always put Routes at end
from todo_project import routes
