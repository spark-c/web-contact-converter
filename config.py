# used to set config / environment vars for web-contact-kidslinkedConverter
# Collin Sparks, cklsparks@gmail.com, https://github.com/spark-c/web-contact-converter

import os

class Config():
    DEBUG = false
    # SESSION_COOKIE_SECURE=True, # free Heroku apps are not HTTPS and session cookie cannot be set as secure
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
    SECRET_KEY = 'kidslinked'
    DL_DIRECTORY = os.path.join(app.instance_path, 'generated')


class DevelopmentConfig():
    SQLALCHEMY_DATABASE_URI = ''


class ProductionConfig():
    pass
