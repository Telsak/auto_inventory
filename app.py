from flask import Flask, render_template
from openpyxl import load_workbook
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

def verify_barcode(payload):
    if len(payload) == 9:
        # check if its a CNAP qr code
        if payload[0:4] == 'CNAP' and payload[4:].isnumeric():
            return True, 'CNAP'
        elif payload[0:2] == 'IT' and payload[2:].isnumeric():
            return True, 'IT'
        else:
            return False, ''
    else:
        # neither of these, or corrupt data
        return False, ''

def cnap_to_itnumber(cnapdata):
    wb = load_workbook(os.path.join(basedir, 'CNAP_utrustning_inventarie.xlsx'))
    ws = wb['Inventarie']
    for row in ws['D']:
        if cnapdata == row.value:
            it_cell = ws[f'E{row.row}'].value
            if len(it_cell) > 0:
                if 'IT' in it_cell:
                    ifttt_message(it_cell, verify_scantoken('IFTTT_key', 'NULL'))
    wb.close()
    return

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
        elif 'IT' in data or 'CNAP' in data:
            # ITnr, check it and process if valid
            result, verify = verify_barcode(data)
            if result:
                ifttt_message(data, verify_scantoken('IFTTT_key', 'NULL'))
                if verify == 'CNAP':
                    cnap_to_itnumber(data)
                    return(f'{verify.upper()} code', data)
                else:
                    return(f'{verify.upper()} code', data)
            else:
                return(f'token ok: {data} invalid')
        else:
            return f'token ok: {data} invalid'
    else:
        return 'failure'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')