"""
App Initializer
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)

  # Register blueprints
  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp)

  from app.main import bp as main_bp
  app.register_blueprint(main_bp)  

  return app