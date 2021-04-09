
from flask import request, render_template, jsonify, send_file, make_response, session, redirect, url_for, abort
import json
import os

from web_contact_converter import app
from web_contact_converter.kidslinkedConverter import kidslinkedConverter as kc
import web_contact_converter.manage_db as mdb


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
