########################################################
# pip install flask
# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# To run:
# $ export FLASK_APP=application.py
# $ flask run
########################################################

from flask import Flask, request, redirect, url_for, render_template, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from src.recognize_text import get_letters_from_image
# import recognize_text
import json, os
import base64


app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'jpg', 'png', 'gif', 'bmp'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ------- Application ------- #


# 1. This endpoint is designed to work with the web cam
@app.route('/', methods=['GET', 'POST'])
def capture_camera_upload():
    import cv2
    import random
    import numpy as np
    if request.method == 'POST':
        # convert string of image data to uint8
        file = str(request.data)
        file = file.split(';')[-1]
        file = file.split(',')[-1]

        imgData = base64.b64decode(file)
        filename = UPLOAD_FOLDER + 'test_image.png'
        print(filename)
        imgFile = open(filename, 'wb')
        imgFile.write(imgData)
        imgFile.close()
        results = get_letters_from_image(filename, debug=True)
        print(results)
        return jsonify(results)
    else:
        return render_template('camera.html')

# 2. This endpoint is designed to work with an uploaded image
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
           results = get_letters_from_image(UPLOAD_FOLDER + filename)
           return render_template('uploader.html', results=results )
    return render_template('uploader.html')


# 3. This endpoint is designed to work with an image that's saved in src/images
@app.route('/get-letters/')
def get_letters():
    return jsonify(get_letters_from_image('src/images/letters_3.jpg'))

if __name__ == '__main__':
    app.run()

