import string
from flask import Flask, jsonify, render_template, request
import werkzeug
import os
import random
from os import walk
from PIL import Image
import config
from instabot import Bot


app = Flask(__name__)
base_img_path = 'static/img/base_img.JPG'
bot = Bot()
print(os.environ)
bot.login(username=os.environ['USERNAME'], password=os.environ['PASSWORD'])


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/upload", methods=['POST'])
def upload():
    imagefile = request.files['file']
    filename = werkzeug.utils.secure_filename(imagefile.filename)
    new_filename = random_string(64)
    imagefile.save(os.path.join("uploads", new_filename))

    with Image.open(base_img_path) as base_img:
        base_img.load()
        with Image.open(os.path.join("uploads", new_filename)) as img:
            img.load()
            base_img.paste(
                img.resize((520, 450)),
                (275, 123)
            )
            base_img.save(os.path.join(
                "uploads", new_filename + "_edited.jpg"))
            bot.upload_photo(new_filename + "_edited.jpg")

    return str(new_filename)


@app.route("/getImages")
def getImages():
    return jsonify(next(walk("uploads/"), (None, None, []))[2])


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))
