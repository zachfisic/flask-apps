"""App package for Microblog tutorial

TODO:
  * Further documentation

Modules:
  app: instance of Flask
  db: ORM via SQLAlchemy
  migrate: Flask wrapper for Alembic database migrator
  login: instance of login manager for handling login persistence
  route: routing logic
  models: database models for microblog
  errors: error handling module
  mail: mail router
"""

import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from flask_login import LoginManager
import os
from config import Config

# Instantiate Flask with the currently named module ("app")
# The 'app' variable below is a member of 'app' package defined by this directory
app = Flask(__name__)

# Instantiate Config class from `config` module. Class variables exist on app.config
app.config.from_object(Config)

mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

# If not in debug mode...
if not app.debug:
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

# Import modules at bottom to prevent circular dependency
# The 'app' variable defined in this file needs to be available for these modules
from app import routes, models, errors