from flask import Flask, request, render_template, jsonify, make_response, session
import infoScrape


app = Flask(__name__)
app.secret_key = 'kidslinked'

@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
        return render_template('index.html')

@app.route('/py_compile', methods=['POST'])
def py_compile():
    print('got a thing')
    #receive JSON request from frontend
    req = request.get_json()
    print(req)
    #do work

    #return response object
    response = make_response(jsonify({'PLACEHOLDER OUTPUT': 'PLACEHOLDER VALUE'}), 200)
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
