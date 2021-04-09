from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_migrate import Migrate
from pathlib import Path

path = Path('.')

app = Flask(__name__)
db = SQLAlchemy(app)
app.config.from_pyfile(str(path.parent.absolute()) + '/config.cfg')
from web_contact_converter.models.Models import Companies, Details
db.create_all()

migrate = Migrate(app, db)

from web_contact_converter import routes
