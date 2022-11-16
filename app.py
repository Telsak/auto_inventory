from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan/<token>/<data>')
def scan(token='', data=''):
    return 'What the fuck!'

if __name__ == '__main__':
    app.run()