# used to set config / environment vars for web-contact-kidslinkedConverter
# Collin Sparks, cklsparks@gmail.com, https://github.com/spark-c/web-contact-converter

import os


class Config():
    DEBUG = False
    # SESSION_COOKIE_SECURE=True, # free Heroku apps are not HTTPS and session cookie cannot be set as secure
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SECRET_KEY = 'kidslinked'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:admin@localhost:5432/web-contact-converter-dev'
    DEBUG = True

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

