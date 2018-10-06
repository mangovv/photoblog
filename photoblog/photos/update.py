from flask import render_template, request, Blueprint

import os

photos = Blueprint('photos',__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@photos.route('/test')
def test():
    return render_template("upload.html")

@photos.route('/upload',methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "images\\")
    #print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    for file in request.files.getlist("file"):
        #print(file)
        filename = file.filename
        destination = "/".join(target).join(filename)
        print('****************************************'+filename+'***************************************')
        print(destination)
        file.save(destination)
    return render_template("complete.html")