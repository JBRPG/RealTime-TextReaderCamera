########################################################
# pip install flask
# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# To run:
# $ export FLASK_APP=application.py
# $ flask run
########################################################

#########
# resource for upload test - Will work more
# https://viveksb007.github.io/2018/04/uploading-processing-downloading-files-in-flask
#########


from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from src.recognize_text import get_letters_from_image
# import recognize_text
import json, os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------- Application ------- #
@app.route('/')
def show_game():
    return render_template('index.html', name='Unknown User')

@app.route('/get-letters/')
def get_letters():
    return jsonify(get_letters_from_image('src/images/letters_3.jpg'))

@app.route('/get-letters-tiles/')
def get_letters_tiles():
    return jsonify(get_letters_from_image('src/images/tiles.png'))

@app.route('/uploader/', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
       #print(UPLOAD_FOLDER)
       if 'file' not in request.files:
           print('No file attached in request')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           print('No file selected')
           return redirect(request.url)
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
           #process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
           results = get_letters_from_image(UPLOAD_FOLDER + filename)
           # jsonify(get_letters_from_image(UPLOAD_FOLDER + filename))
           # return redirect(url_for('uploader', filename=filename))
           return render_template('uploader.html', results=results )
    return render_template('uploader.html')
