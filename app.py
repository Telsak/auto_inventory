from flask import Flask, render_template
import os, json

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

def verify_scantoken(token_type, token):
    '''verifies the token or key against the user json file'''
    if len(token) > 0:
        with open(os.path.join(basedir, 'users.crd')) as file:
            json_data = json.load(file)
            for user in json_data["user_tokens"]:
                if user[token_type] == token:
                    return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan/<token>/<data>')
def scan(token='', data=''):
    if verify_scantoken("scan_token", token):
        return f'success {data}'
    else:
        return 'failure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')