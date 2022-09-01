# PACKAGE STRUCTURE
# package is called app
# all imports are 'from app import'
# models.py contains db Models - Imported here
# routes.py contains all routes
# config.py sets Flask app configuration variables
# __init__.py starts the Flask app and brings everything together
# static and templates folders are all located here

# set persistent env variables using setx NAME "BLAH"

# This is the flask app constructor
from flask import Flask
from app.config import Config, DevelopmentConfig, TestingConfig

# setting the app variable
app = Flask(__name__)

# Updates the config state
if app.config["ENV"] == "production":
    app.config.from_object("app.config.ProductionConfig")
elif app.config["ENV"] == "testing":
    app.config.from_object("app.config.TestingConfig")
else:
    app.config.from_object("app.config.DevelopmentConfig")

from app import views
from app import admin_views

# in POWERSHELL
# $env:FLASK_ENV = "development"