# Flask code for the module "web-contact-converter", a web app used to generate spreadsheets from contact information
# Collin Sparks, cklsparks@gmail.com, https://github.com/spark-c/web-contact-converter

from flask import Flask, request, render_template, jsonify, send_file, make_response, session, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
import os

from kidslinkedConverter import kidslinkedConverter as kc
from Models import Companies, db
import manage_db as mdb


app = Flask(__name__)

# app.secret_key = 'kidslinked'
# app.config.update(
#     # SESSION_COOKIE_SECURE=True, # Commented out for use on Heroku becuase free apps are not HTTPS and session cookie cannot be set as secure
#     SESSION_COOKIE_HTTPONLY=True,
#     SESSION_COOKIE_SAMESITE='Lax'
# )
# print('path {}'.format(app.instance_path))
# app.config['DL_DIRECTORY'] = os.path.join(app.instance_path, 'generated')

print(os.environ["APP_SETTINGS"])


@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    if not session.get('user_id'):
        session['user_id'] = mdb.generate_id()

    companies_in_session = mdb.fetch_from_db(session['user_id']) # if user_id in session, returns their companies. otherwise, return []
    return render_template('index.html', total_companies=len(companies_in_session))


@app.route('/compile_from_session', methods=['POST', 'GET'])
def compile_from_session(): # sends the companies currently in the session
    response = make_response(jsonify(companies_in_session), 200)
    return response


@app.route('/py_compile', methods=['POST', 'GET'])
def py_compile(): # takes request containing new companies and processes/stores them.
    new_companies = []
    req = request.get_json()
    for company in kc.compile_for_remote(req): # for loop, otherwise we get nested lists which complicates json
        new_companies.append(company)
        mdb.add_to_db(session['user_id'], company)

    companies_in_session = mdb.fetch_from_db(session['user_id']) # update master list to include new companies

    response = make_response(jsonify(new_companies), 200)
    return response


@app.route('/py_generate', methods=['POST', 'GET'])
def py_generate(): # generates spreadsheet from data in session. spreadsheet is created in ./instance directory and sent to the user
    wb = kc.generate_wb(companies_in_session)
    filepath = app.config['DL_DIRECTORY'] + 'output.xlsx'
    with open(filepath, 'wb') as temp:
        wb.save(temp)
        temp.seek(0)

    response = send_file(app.config['DL_DIRECTORY'] + 'output.xlsx',
    mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    attachment_filename='output.xlsx',
    as_attachment=True
    )
    try:
        return response
    except FileNotFoundError:
        abort(404)


@app.route('/delete_selected', methods=['POST','GET'])
def delete_selected():
    delete_keys = list() # this will be our key for which companies to delete (using emails, since those are unique)
    for entry in request.form: # each entry is an email
        delete_keys.append(entry)

    mdb.delete_from_db(session['user_id'], delete_keys)
    companies_in_session = mdb.fetch_from_db(session['user_id'])

    return redirect(url_for('home'))


@app.route('/delete_all', methods=['POST', 'GET'])
def delete_all():
    print('deleting all')
    mdb.delete_from_db(session['user_id'])
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run()
