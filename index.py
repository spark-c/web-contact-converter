from flask import Flask, request, render_template, jsonify, make_response, session
import json
from kidslinkedConverter import kidslinkedConverter as kc
import datetime


app = Flask(__name__)
app.secret_key = 'kidslinked'
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=1)
SESSION_COOKIE_SECURE = True

# all_companies = []


@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
        if session.get('all_companies'): # checks if the key exists
            return render_template('index.html', session_data=True, total_companies=len(session['all_companies'])) # tell js to load session data to page
        else:
            session['all_companies'] = []
            return render_template('index.html', session_data=False, total_companies=len(session['all_companies'])) # clean load of page

@app.route('/py_compile', methods=['POST'])
def py_compile():
    new_companies = []
    print('got a thing')
    #receive JSON request from frontend
    req = request.get_json()
    print(req)
    for company in kc.compile_for_remote(req): # for loop, otherwise we get nested lists which complicates json
        new_companies.append(company)
        session['all_companies'].append(company)

    #return response object
    print(new_companies)
    response = make_response(jsonify(new_companies), 200)
    # return render_template('index.html')
    return response

@app.route('/py_generate', methods=['POST', 'GET'])
def py_generate():
    pass

@app.route('/py_delete', methods=['POST','GET'])
def py_delete():
    pass


if __name__ == '__main__':
    app.run()
