from flask import render_template, request, Blueprint
from wand.image import Image
from wand.api import library
import ctypes
#add session

import os

photos = Blueprint('photos',__name__)
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destination = ""

@photos.route('/upload')
def test():
    return render_template("upload.html")

@photos.route('/test/FileUpload',methods=["POST"])
def upload():
    target = os.path.join(APP_ROOT, "static\\")
    if not os.path.isdir(target):
        os.mkdir(target)
    for new_file in request.files.getlist("uploadedfile"):
        name, ext = new_file.filename.split('.')
        ext = '.' +ext
        filename0 = name+ext
        filename1 = name+'_1'+ext
        filename2 = name+'_2'+ext
        filename3 = name+'_3'+ext
        destination0 = target + filename0
        destination1 = target + filename1
        destination2 = target + filename2
        destination3 = target + filename3

        with Image(file = new_file) as image:
            image.save(filename=destination0)
            transform_upload(destination0,destination1,destination2,destination3)

    return render_template("complete.html")

def transform_upload(destination0, destination1, destination2, destination3):
    img = Image(filename=destination0)
    transformed1 = img.clone()
    transformed2 = img.clone()
    transformed3 = img.clone()

    library.MagickSepiaToneImage.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickSepiaToneImage.restype = None

    transformed1.resize(50,50)
    transformed2.type = 'grayscale'
    transformed3.rotate(270)

    threshold = transformed3.quantum_range * 0.8
    library.MagickSepiaToneImage(transformed3.wand, threshold)

    transformed1.save(filename= destination1)
    transformed2.save(filename= destination2)
    transformed3.save(filename= destination3)

@photos.route('/display')
def display():
    return render_template('display.html', user_name='tianyue', image_list=[destination])