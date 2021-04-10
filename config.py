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
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # This doesn't seem to work. SQLAlchemy wants "postgresql" prefix but heroku forces it to be "postgres".
    SQLALCHEMY_DATABASE_URI = 'postgresql://iasxannxrruajn:b53405936ee738d40f581a11f410a48765bce03781bb67cdb33682caf8b6b41e@ec2-18-233-83-165.compute-1.amazonaws.com:5432/dampp0gl7t506a'

