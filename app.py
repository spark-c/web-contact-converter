# Flask code for the module "web-contact-converter", a web app used to generate spreadsheets from contact information
# Collin Sparks, Feb 2021
# Python 3
from flask import Flask, request, render_template, jsonify, send_file, send_from_directory, make_response, session, redirect, url_for, abort
import json
from kidslinkedConverter import kidslinkedConverter as kc
import datetime
import os
import sys
import logging
from logging import Formatter

def log_to_stderr(app):     # this function copied from https://stackoverflow.com/questions/26819050/running-flask-app-on-heroku
                            # to help with debugging heroku deployment.
  handler = logging.StreamHandler(sys.stderr)
  handler.setFormatter(Formatter(
    '%(asctime)s %(levelname)s: %(message)s '
    '[in %(pathname)s:%(lineno)d]'
  ))
  handler.setLevel(logging.WARNING)
  app.logger.addHandler(handler)


app = Flask(__name__)
app.secret_key = 'kidslinked'

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)
print('path {}'.format(app.instance_path))
app.config['DL_DIRECTORY'] = os.path.join(app.instance_path, 'generated')


# all_companies = []


@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
        if session.get('all_companies'): # checks if the key exists
            print(session['all_companies'])
            return render_template('index.html', session_data=True, total_companies=len(session['all_companies'])) # tell js to load session data to page
        else:
            session['all_companies'] = []
            return render_template('index.html', session_data=False, total_companies=len(session['all_companies'])) # clean load of page


@app.route('/compile_from_session', methods=['POST', 'GET'])
def compile_from_session():
    print('in function')
    response = make_response(jsonify(session['all_companies']), 200)
    print(response)
    return response


@app.route('/py_compile', methods=['POST', 'GET'])
def py_compile():
    new_companies = []
    temp = session['all_companies'] # saves all companies in memory to temporary list
    #receive JSON request from frontend
    req = request.get_json()
    for company in kc.compile_for_remote(req): # for loop, otherwise we get nested lists which complicates json
        new_companies.append(company)
        temp.append(company)
    session['all_companies'] = temp # store updated master list in session
    #return response object
    response = make_response(jsonify(new_companies), 200)
    # return render_template('index.html')
    return response

@app.route('/py_generate', methods=['POST', 'GET'])
def py_generate():
    temp = session['all_companies']

    # doc_title = req['message']
    print('session: {} companies'.format(len(temp)))
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
        print('sending... ')
        return response
    except FileNotFoundError:
        abort(404)


@app.route('/py_delete', methods=['POST','GET'])
def py_delete():
    pass


@app.route('/delete_all', methods=['POST', 'GET'])
def delete_all():
    session['all_companies'] = []
    return redirect(url_for('home'))


if __name__ == '__main__':
    log_to_stderr(app)
    app.run()
