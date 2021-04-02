# Models for the postgres database used in web-contact-kidslinkedConverter
# Collin Sparks, cklsparks@gmail.com, https://github.com/spark-c/web-contact-converter

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func

db = SQLAlchemy()


class Companies(db.Model):
    __tablename__ = 'companies'

    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=True)

    date_created = db.Column(db.DateTime(timezone=True), nullable=False, default=func.now())
    user_id = db.Column(db.String, nullable=False)
    company_id = db.Column(db.String, nullable=False)
    details = db.relationship('Details', backref='companies', lazy=False)


class Details(db.Model):
    __tablename__ = 'details'

    id = db.Column(db.Integer, primary_key=True) # SQLAlchemy should take care of populating this column automatically
    company_id = db.Column(db.String, db.ForeignKey('companies.company_id'), nullable=False)
    
    contacts = db.Column(db.String, nullable=True)
    emails = db.Column(db.String, nullable=True)
    phones = db.Column(db.String, nullable=True)
