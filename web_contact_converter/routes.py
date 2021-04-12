
from flask import request, render_template, jsonify, send_file, make_response, session, redirect, url_for, abort
from time import sleep
import json
import os

from web_contact_converter import app
from kidslinkedConverter import kidslinkedConverter as kc
import web_contact_converter.manage_db as mdb


@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    if not session.get('user_id'):
        session['user_id'] = mdb.generate_id()

    return render_template('index.html', total_companies=mdb.fetch_from_db(session['user_id'], count=True))


@app.route('/compile_from_session', methods=['POST', 'GET'])
def compile_from_session(): # sends the companies currently in the session
    companies_in_session = mdb.fetch_from_db(session['user_id'])
    response = make_response(jsonify([x.__dict__ for x in companies_in_session]), 200) # list comprehension b/c objects not JSON serializable

    return response


@app.route('/py_compile', methods=['POST', 'GET'])
def py_compile(): # takes request containing new companies and processes/stores them.
    new_companies = []
    req = request.get_json()
    for company in kc.compile_for_remote(req): # for loop, otherwise we get nested lists which complicates json
        new_companies.append(company)
    mdb.add_to_db(session['user_id'], new_companies)

    companies_in_session = mdb.fetch_from_db(session['user_id']) # update master list to include new companies

    response = make_response(jsonify(new_companies), 200)
    return response


@app.route('/py_generate', methods=['POST', 'GET'])
def py_generate(): # generates spreadsheet from data in session. spreadsheet is created in ./instance directory and sent to the user
    companies_in_session = mdb.fetch_from_db(session['user_id'])
    wb = kc.generate_wb([obj.__dict__ for obj in companies_in_session]) # this function expects a list
    filepath = os.path.join(os.path.dirname(app.instance_path), 'web_contact_converter\\output\\output.xlsx')
    with open(filepath, 'wb') as temp:
        wb.save(temp)
        temp.seek(0)

    response = send_file(filepath,
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
    if len(request.form) > 1:
        key_dict = request.form.to_dict(flat=True)
        key_dict.pop('delete')
        delete_keys = key_dict.keys()
        print('delete keys:', delete_keys)

        mdb.delete_from_db(session['user_id'], delete_keys)
        companies_in_session = mdb.fetch_from_db(session['user_id'])

    return redirect(url_for('home'))


@app.route('/delete_all', methods=['POST', 'GET'])
def delete_all():
    print('deleting all')
    mdb.delete_from_db(session['user_id'])
    return redirect(url_for('home'))
