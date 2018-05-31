"""
Configuration Settings
"""

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):

  SECRET_KEY = os.environ.get('SECRET_KEY')
  """str: cryptographic key, used to generate signatures and tokens."""

  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
  """str: URI for application database."""

  SQLALCHEMY_TRACK_MODIFICATIONS = False
  """bool: setting for modification tracking."""