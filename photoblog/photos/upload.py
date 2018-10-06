from flask import render_template, request, Blueprint

import os

photos = Blueprint('photos',__name__)
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destination = ""

@photos.route('/test')
def test():
    return render_template("upload.html")

@photos.route('/upload',methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "static\\")
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        filename = file.filename
        destination = target+filename
        print(destination)
        file.save(destination)
    return render_template("complete.html")

@photos.route('/display')
def display():
    return render_template('display.html', user_name='tianyue', image_list=[destination])