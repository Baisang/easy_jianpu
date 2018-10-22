import io

from flask import flash
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file

from helpers import convert_jianpu_to_jianpu
from helpers import convert_jianpu_to_midi
from helpers import convert_jianpu_to_western
from helpers import generate_random_filename

app = Flask(__name__)
app.secret_key = b'thisisnotasecretkey'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/jianpu', methods=['POST'])
def convert_jianpu():
    mimetype = 'application/pdf'
    extension = 'pdf'
    if request.form['format'] == 'western':
        file = convert_jianpu_to_western(request.form['jianpu'])
    elif request.form['format'] == 'jianpu':
        file = convert_jianpu_to_jianpu(request.form['jianpu'])
    elif request.form['format'] == 'midi':
        file = convert_jianpu_to_midi(request.form['jianpu'])
        mimetype = 'audio/midi'
        extension = 'midi'
    if type(file) != io.BytesIO:
        flash(file)
        return render_template('index.html', input=request.form['jianpu'])

    return send_file(
        file,
        as_attachment=True,
        attachment_filename=generate_random_filename(extension),
        mimetype=mimetype,
    )
