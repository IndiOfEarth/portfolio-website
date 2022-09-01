# Creating a configuration file for the Flask app

# Base Config() parent class
class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "CYBGAg79IVxXp6kAc9gAAA" # Generated with Python Secrets Module
    DB_NAME = "production-db" # The db file that is used for different config states
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///personal-website.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_PATH = 'static/img'

# Child classes that will inherit the Config() parent class
# These are different config states
class ProductionConfig(Config):
    ENV = "production"

class DevelopmentConfig(Config):
    ENV = "development"
    DEBUG = True
    DB_NAME = "development-db"
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True
    DB_NAME = "development-db"
    SESSION_COOKIE_SECURE = False
