import string
from flask import Flask, render_template, request
import werkzeug
import os
import random


app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/upload", methods=['POST'])
def upload():
    imagefile = request.files['file']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    new_filename = random_string(64)
    imagefile.save(os.path.join("uploads", new_filename))

    return str(new_filename)

def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))
