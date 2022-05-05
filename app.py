import string
from flask import Flask, jsonify, render_template, request
import werkzeug
import os
import random
from os import walk
from PIL import Image
from instauto.api.client import ApiClient
from instauto.helpers.post import upload_image_to_feed


app = Flask(__name__)
base_img_path = 'static/img/base_img.JPG'
client = ApiClient.initiate_from_file('store.instauto')


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/init")
def init():
    client = ApiClient(username=os.environ['USERNAME'],
                       password=os.environ['PASSWORD'])
    client.log_in()
    client.save_to_disk('store.instauto')
    return jsonify({'status': 'ok'})


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
            upload_image_to_feed(client, "./uploads/" + new_filename + "_edited.jpg",
                                 "test")

    return str(new_filename)


@app.route("/getImages")
def getImages():
    return jsonify(next(walk("uploads/"), (None, None, []))[2])


def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for x in range(length))
