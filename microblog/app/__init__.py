"""
App package for Microblog tutorial

TODO:
  * Further documentation
  * Translations
  * Language guessing
"""

import os
import logging
from config import Config
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask, request, current_app
from flask_babel import Babel, lazy_gettext as _l
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from elasticsearch import Elasticsearch

# Create instances for all extensions
db = SQLAlchemy()
mail = Mail()
migrate = Migrate()
moment = Moment()
babel = Babel()
bootstrap = Bootstrap()
login = LoginManager()
login.login_view = 'auth.login'
login.login_message = _l('Please log in to access this page.')


def create_app(config_class=Config):
  # Instantiate Flask with the currently named module ("app")
  # The 'app' variable below is a member of 'app' package defined by this directory
  app = Flask(__name__)

  # Instantiate Config class from `config` module. Class variables exist on app.config
  app.config.from_object(Config)
  
  # Add elasticsearch
  app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None

  # Initialize extensions with app instance
  db.init_app(app)
  mail.init_app(app)
  migrate.init_app(app, db)
  moment.init_app(app)
  babel.init_app(app)
  bootstrap.init_app(app)
  login.init_app(app)

  # Register Blueprints
  from app.errors import bp as errors_bp
  app.register_blueprint(errors_bp)

  from app.auth import bp as auth_bp
  app.register_blueprint(auth_bp, url_prefix='/auth')

  from app.main import bp as main_bp
  app.register_blueprint(main_bp)

  # Mail and log settings for production
  if not app.debug and not app.testing:
    if app.config['MAIL_SERVER']:
      auth = None
      if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
      secure = None
      if app.config['MAIL_USE_TLS']:
        secure = ()
      mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'],
        subject='Microblog failure',
        credentials=auth,
        secure=secure
      )
      mail_handler.setLevel(logging.ERROR)
      app.logger.addHandler(mail_handler)

    if not os.path.exists('logs'):
      os.mkdir('logs')
      file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240, backupCount=10)
      file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
      file_handler.setLevel(logging.INFO)
      app.logger.addHandler(file_handler)
      app.logger.setLevel(logging.INFO)
      app.logger.info('Microblog startup')

  return app


@babel.localeselector
def get_locale():
  return request.accept_languages.best_match(current_app.config['LANGUAGES'])
  


# Import modules at bottom to prevent circular dependency
# The 'app' variable defined in this file needs to be available for these modules
from app import models