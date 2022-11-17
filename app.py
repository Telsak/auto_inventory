from flask import Flask, render_template
import os, json, requests

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['CURRENTROOM'] = ''

def verify_scantoken(token_type, token):
    '''verifies the token or key against the user json file'''
    if len(token) > 0:
        with open(os.path.join(basedir, 'users.crd')) as file:
            json_data = json.load(file)
            for user in json_data['user_tokens']:
                if token_type == 'IFTTT_key':
                    return user[token_type]
                else:
                    if user[token_type] == token:
                        return True
    return False

def ifttt_message(payload, key):
    msg_data = {}
    msg_data['value1'] = payload
    requests.post(f'https://maker.ifttt.com/trigger/notify/with/key/{key}', data=msg_data)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scan/<token>/<data>')
def scan(token='', data=''):
    if verify_scantoken('scan_token', token):
        # if data is a tuple with a room/number: ie. ('set_room', 'b112')
        if 'set_room' in data:
            from flask import current_app
            room = current_app.config['CURRENTROOM'] = data.split(':')[1]
            ifttt_message(f'room changed to {room}', verify_scantoken('IFTTT_key', 'NULL'))
        elif 'IT' in data:
            # ITnr, check it and process if valid
            return('IT number')
        elif 'CNAP' in data:
            # CNAP QR code, check it and process if valid
            return('CNAP qr code')
        return f'success {data}'
    else:
        return 'failure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')