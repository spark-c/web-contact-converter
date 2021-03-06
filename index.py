from flask import Flask, request, render_template, jsonify, send_file, make_response, session, redirect, url_for
import json
from kidslinkedConverter import kidslinkedConverter as kc
import datetime
from tempfile import NamedTemporaryFile
import os
from io import BytesIO


app = Flask(__name__)
app.secret_key = 'kidslinked'

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax'
)


UPLOAD_FOLDER = 'generated'

# all_companies = []


@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
        if session.get('all_companies'): # checks if the key exists
            print(session['all_companies'])
            return render_template('index.html', session_data=True, total_companies=len(session['all_companies'])) # tell js to load session data to page
        else:
            print(session['all_companies'])
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

@app.route('/py_generate', methods=['GET'])
def py_generate():
    temp = session['all_companies']



    print(temp)
    req = request.get_json()
    # doc_title = req['message']
    print('session: {}'.format(temp))
    wb = kc.generate_wb(temp)
    filepath = app.instance_path + '\\generated\\output.xlsx'
    with open(filepath, 'wb') as temp:
        wb.save(temp)
        temp.seek(0)

    # saved_location = kc.convert_to_wb(dest_path, session['all_companies'], doc_title)
    # response = make_response(stream, 200)
    # response.headers['content-type'] = 'application'
    # mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    # direct_passthrough=True,
    # )
    return send_file(filepath, as_attachment=True, attachment_filename='output.xlsx')


@app.route('/py_delete', methods=['POST','GET'])
def py_delete():
    pass


@app.route('/delete_all', methods=['POST', 'GET'])
def delete_all():
    session['all_companies'] = []
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run()
