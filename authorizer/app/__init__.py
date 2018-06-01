"""
App Initializer
"""

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize extensions
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = 'Please log in to access this page.'

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  # Load extensions on app
  db.init_app(app)
  login.init_app(app)

  # Register blueprints
  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp)

  from app.main import bp as main_bp
  app.register_blueprint(main_bp)  

  return app