# Contains functions used to liase between web-contact-converter backend and database.
# Collin Sparks, cklsparks@gmail.com, https://github.com/spark-c/web-contact-kidslinkedConverter

from flask_sqlalchemy import SQLAlchemy
import secrets

from Models import Companies, db


def generate_id():
    id = secrets.token_hex(4)
    return id


def add_to_db(user_id, company_obj): # takes str user_id, list of objs
    pass


def delete_from_db(user_id, company_obj): # takes str user_id, list of keys to query for deletion
    pass


def fetch_from_db(user_id): # return list of companies belonging to passed user_id
    pass
