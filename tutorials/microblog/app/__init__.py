from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# import routes at bottom to prevent circular module importing
from app import routes