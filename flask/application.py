########################################################
# pip install flask
# https://flask.palletsprojects.com/en/1.1.x/quickstart/
# To run: 
# $ export FLASK_APP=application.py
# $ flask run
########################################################

from flask import Flask, render_template, jsonify
import json
app = Flask(__name__)

@app.route('/')
def show_game():
    return render_template('index.html', name='Unknown User')

@app.route('/get-letters/')
def get_letters():
    from src.recognize_text import get_letters_from_image
    return jsonify(get_letters_from_image('src/images/letters_3.jpg'))

   