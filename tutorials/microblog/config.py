"""Configuration file

This file lives outside the main application. Settings here are defined as class variables inside a `Config` class.

In production applications, this file should exist outside VC.

"""
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
  """Class for representing app settings."""

  LANGUAGES = ['en_US', 'es_ES']
  """list: translated languages"""

  POSTS_PER_PAGE = 3
  """int: pagination setting"""

  MAIL_SERVER = os.environ.get('MAIL_SERVER')
  """str: designated email server."""

  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
  """int: designated email port."""

  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
  """bool: TLS setting."""

  MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL') is not None
  """bool: SSL setting."""

  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  """str: designated email username."""

  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  """str: designated email password."""

  ADMINS = ['zachfisic@gmail.com']
  """list: email addresses for logging/error notification."""

  SECRET_KEY = os.environ.get('SECRET_KEY') or 'foobar'
  """str: cryptographic key, used to generate signatures and tokens."""

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
  """str: URI for application database."""

  SQLALCHEMY_TRACK_MODIFICATIONS = False
  """bool: setting for modification tracking."""