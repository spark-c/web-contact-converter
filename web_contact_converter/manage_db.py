# Contains functions used to liase between web-contact-converter backend and database.
# Collin Sparks, cklsparks@gmail.com, https://github.com/spark-c/web-contact-kidslinkedConverter

from sqlalchemy.orm import selectinload
import secrets

from web_contact_converter import db
from web_contact_converter.models.Models import Companies, Details
from web_contact_converter.kidslinkedConverter import Company


tmp = db.session.query(Companies).all() # These two lines create a set of all ids in use, to prevent creating duplicates
used_ids = set([Companies.company_id for i in tmp] + [Companies.user_id for i in tmp])
print('USED_IDS: {}'.format(used_ids))


def generate_id():
    while True: # loop until we get a unique ID
        id = secrets.token_hex(4)
        if id not in used_ids:
            return id


def build(db_result): # builds a Company object from a db query result
    newObj = Company(db_result.name)
    for detail in db_result.details: # should be iterating through relevant detail rows in Details table
        newObj.add(detail.type, detail.data)

    return newObj


def add_to_db(user_id, company_obj): # takes str user_id, list of objs
    for obj in company_obj:
        newCompanyID = generate_id()

        newCompany = Companies(name=obj.name, user_id=user_id, company_id=newCompanyID)
        db.session.add(newCompany)

        for info in obj.contacts:
            newDetail = Details(company_id=newCompanyID, type='contact', data=info)
            db.session.add(newDetail)
        for info in obj.emails:
            newDetail = Details(company_id=newCompanyID, type='email', data=info)
            db.session.add(newDetail)
        for info in obj.phones:
            newDetail = Details(company_id=newCompanyID, type='phone', data=info)
            db.session.add(newDetail)
        for info in obj.address:
            newDetail = Details(company_id=newCompanyID, type='address', data=info)
            db.session.add(newDetail)

        db.session.commit()


def delete_from_db(user_id, keys): # takes str user_id, list of keys to query for deletion
    # objects = []
    # for key in keys:
    #     objects.append(Companies.query.filter_by(email))
    pass


def fetch_from_db(user_id): # return list of company objs belonging to passed user_id
    objects = []
    results = db.session.query(Companies).\
        options(selectinload(Companies.details)).\
        filter_by(user_id=user_id).\
        all()

    for company in results:
        objects.append(build(company))

    return objects
