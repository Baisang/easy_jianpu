from flask import Flask
from flask import flash
from flask import request
from flask import send_file
from flask import render_template

from helpers import convert_jianpu_to_western
from helpers import convert_jianpu_to_jianpu

app = Flask(__name__)
app.secret_key = b'thisisnotasecretkey'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/jianpu', methods=['POST'])
def convert_jianpu():
    if request.form['format'] == 'western':
        pdf = convert_jianpu_to_western(request.form['jianpu'])
    elif request.form['format'] == 'jianpu':
        pdf = convert_jianpu_to_jianpu(request.form['jianpu'])
    if type(pdf) != str:
        flash(pdf)
        return render_template('index.html', input=request.form['jianpu'])
    return send_file(pdf)
