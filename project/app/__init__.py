import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

app_settings = os.getenv(
    'APP_SETTINGS',
    'project.app.config.Config'
)

app.config.from_object(app_settings)

db = SQLAlchemy(app)

CORS(app)
