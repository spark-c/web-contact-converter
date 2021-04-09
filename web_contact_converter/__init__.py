from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
import os


app = Flask(__name__)
app.config.from_object(os.getenv("APP_SETTINGS"))
db = SQLAlchemy(app)

# app.config.from_pyfile(str(path.parent.absolute()) + '/config.cfg')
from web_contact_converter.models.Models import Companies, Details
db.create_all()

migrate = Migrate(app, db)

from web_contact_converter import routes
