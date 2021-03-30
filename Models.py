# Models for the postgres database used in web-contact-kidslinkedConverter
# Collin Sparks, cklsparks@gmail.com, https://github.com/spark-c/web-contact-converter

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func

db = SQLAlchemy()


class Companies(db.Model):
    __tablename__ = 'companies'

    name = db.Column(db.String, nullable=False)
    contacts = db.Column(db.JSON, nullable=False) # these are JSON so we can use lists
    emails = db.Column(db.JSON, nullable=False)
    phones = db.Column(db.JSON, nullable=False)
    address = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
