# Models for the postgres database used in web-contact-kidslinkedConverter
# Collin Sparks, cklsparks@gmail.com, https://github.com/spark-c/web-contact-converter

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON, UUID
import uuid
import datetime

db = SQLAlchemy()

class Companies(db.Model):
    __tablename__ = 'companies'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String, nullable=False)
    contacts = db.Column(db.JSON(), nullable=False) # these are JSON so we can use lists
    emails = db.Column(db.JSON, nullable=False)
    phones = db.Column(db.JSON, nullable=False)
    address = db.Column(db.String, nullable=False)
    user_id = db.Column(db.String, nullable=False)
