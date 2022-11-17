from flask import Flask, render_template
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

def verify_input(data):
    if len(data) > 0:
        with open(os.path.join(basedir, 'tk.crd')) as file:
            if data == file.readline():
                return True
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan/<token>/<data>')
def scan(token='', data=''):
    if verify_input(token):
        return 'success'
    else:
        return 'What the fuck!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')