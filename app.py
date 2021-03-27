# Flask code for the module "web-contact-converter", a web app used to generate spreadsheets from contact information
# Collin Sparks, Feb 2021
# cklsparks@gmail.com, https://github.com/spark-c/web-contact-converter

from flask import Flask, request, render_template, jsonify, send_file, make_response, session, redirect, url_for, abort
import json
from kidslinkedConverter import kidslinkedConverter as kc
import os


app = Flask(__name__)
app.secret_key = 'kidslinked'
app.config.update(
    # SESSION_COOKIE_SECURE=True, # Commented out for use on Heroku becuase free apps are not HTTPS and session cookie cannot be set as secure
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
print('path {}'.format(app.instance_path))
app.config['DL_DIRECTORY'] = os.path.join(app.instance_path, 'generated')


@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    if session.get('all_companies'): # checks if the key exists
        return render_template('index.html', total_companies=len(session['all_companies']))
    else:
        session['all_companies'] = []
        return render_template('index.html', total_companies=len(session['all_companies'])) # clean load of page


@app.route('/compile_from_session', methods=['POST', 'GET'])
def compile_from_session(): # sends the companies currently in the session
    response = make_response(jsonify(session['all_companies']), 200)
    return response


@app.route('/py_compile', methods=['POST', 'GET'])
def py_compile():
    new_companies = []
    temp = session['all_companies'] # saves all companies to temporary list
    req = request.get_json()
    for company in kc.compile_for_remote(req): # for loop, otherwise we get nested lists which complicates json
        new_companies.append(company)
        temp.append(company)
    session['all_companies'] = temp # store updated master list in session
    response = make_response(jsonify(new_companies), 200)
    return response


@app.route('/py_generate', methods=['POST', 'GET'])
def py_generate(): # generates spreadsheet from data in session. spreadsheet is created in ./instance directory and sent to the user
    temp = session['all_companies']

    wb = kc.generate_wb(temp)
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
    delete_keys = set() # this will be our key for which companies to delete (using emails, since those are unique)
    for entry in request.form: # each entry is a company name
        delete_keys.add(entry)

    current_session = session['all_companies']
    new_session = []
    for index, obj in enumerate(current_session):
        try:
            if obj['emails'][0] not in delete_keys:
                new_session.append(obj)
                print('deleted')
        except:
            print('ERROR, item {} not in list'.format(obj['emails'][0]))
            continue
    session['all_companies'] = new_session
    print('current session at end: {}'.format([obj['emails'] for obj in new_session]))

    return redirect(url_for('home'))


@app.route('/delete_all', methods=['POST', 'GET'])
def delete_all():
    print('deleting all')
    session['all_companies'] = []
    return redirect(url_for('home'))


# @app.route('/echo', methods=['POST', 'GET']) # for debug; echoes in console the text of the request
# def echo():
#     req = request.form
#     print('ECHO:\n{}'.format(req))
#     return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
