from flask import Flask, request, render_template
import infoScrape


app = Flask(__name__)
app.secret_key = 'kidslinked'

@app.route('/home', methods=['POST', 'GET'])
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        pass # form data was submitted so we should be processing
            # probably render a template for a page with a download button
    else:
        return render_template('index.html')
