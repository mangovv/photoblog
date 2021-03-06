from flask import render_template, request, Blueprint, redirect, url_for
from wand.image import Image
from wand.api import library
from photoblog import db
from photoblog.models import User, Photo
import boto3
from flask_login import current_user, login_required

import ctypes
import os

photos = Blueprint('photos', __name__)
APP_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
destination = ""


@photos.route('/upload')
@login_required
def test():
    return render_template("upload.html")

@photos.route('/FileUpload', methods=["POST"])
@login_required
def upload2():
    target = os.path.join(APP_ROOT, "static/")
    if not os.path.isdir(target):
        os.mkdir(target)

    if 'uploadedfile' not in request.files:
        return render_template("filenameerror.html")

    if not request.files.getlist("uploadedfile"):
        return render_template("filenameerror.html")


    for new_file in request.files.getlist("uploadedfile"):
        name, ext = new_file.filename.split('.')
        if ext != ('jpg' or 'jpeg' or 'png' or 'gif' or 'png' or 'tif'):
            return render_template("typeerror.html")
        ext = '.' + ext
        filename0 = name + ext
        filename1 = name + '_1' + ext
        filename2 = name + '_2' + ext
        filename3 = name + '_3' + ext
        filename4 = name + '_4' + ext
        destination0 = target + filename0
        destination1 = target + filename1
        destination2 = target + filename2
        destination3 = target + filename3
        destination4 = target + filename4

        photo = Photo(user_id=current_user.id,
                      title=name,
                      original= filename0,
                      thumbnail=filename1,
                      rotate=filename2,
                      sepia=filename3,
                      black_white=filename4
                      )

        db.session.add(photo)
        db.session.commit()

        s3 = boto3.client('s3')

        with Image(file=new_file) as image:
            image.save(filename=destination0)
            s3.upload_file(destination0, 'ece1779-bucket-1', filename0)
            transform_upload(destination0, destination1, destination2, destination3, destination4, filename1, filename2, filename3, filename4, s3)
            os.remove(destination0)

    return render_template("complete.html")



@photos.route('/test/FileUpload', methods=["POST"])
# @login_required
def upload():
    target = os.path.join(APP_ROOT, "static/")
    if not os.path.isdir(target):
        os.mkdir(target)

    if 'uploadedfile' not in request.files:
        return "Uploaded file is missing in the form"

    if not request.files.getlist("uploadedfile"):
        return "File name is not provided"

    username = request.form['userID']
    user = User.query.filter_by(username=username).first()
    if (not user.check_password(request.form['password'])) or (user is None):
        return redirect(url_for('view.home_page'))

    for new_file in request.files.getlist("uploadedfile"):
        name, ext = new_file.filename.split('.')
        if ext != ('jpg' or 'jpeg' or 'png' or 'gif' or 'png' or 'tif'):
            return "file type not supported"
        ext = '.' + ext
        filename0 = name + ext
        filename1 = name + '_1' + ext
        filename2 = name + '_2' + ext
        filename3 = name + '_3' + ext
        filename4 = name + '_4' + ext
        destination0 = target + filename0
        destination1 = target + filename1
        destination2 = target + filename2
        destination3 = target + filename3
        destination4 = target + filename4

        photo = Photo(user_id=user.id,
                      title=name,
                      original= filename0,
                      thumbnail=filename1,
                      rotate=filename2,
                      sepia=filename3,
                      black_white=filename4
                      )

        db.session.add(photo)
        db.session.commit()

        s3 = boto3.client('s3')

        with Image(file=new_file) as image:
            image.save(filename=destination0)
            s3.upload_file(destination0, 'ece1779-bucket-1', filename0)
            transform_upload(destination0, destination1, destination2, destination3, destination4, filename1, filename2, filename3, filename4, s3)
            os.remove(destination0)

    return render_template("complete.html")


def transform_upload(destination0, destination1, destination2, destination3, destination4, filename1, filename2, filename3, filename4, s3):
    img = Image(filename=destination0)
    transformed1 = img.clone()
    transformed2 = img.clone()
    transformed3 = img.clone()
    transformed4 = img.clone()

    transformed1.resize(1280, 720)
    transformed2.rotate(180)

    library.MagickSepiaToneImage.argtypes = [ctypes.c_void_p, ctypes.c_double]
    library.MagickSepiaToneImage.restype = None
    threshold = transformed3.quantum_range * 0.8
    library.MagickSepiaToneImage(transformed3.wand, threshold)

    transformed4.type = 'grayscale'

    transformed1.save(filename=destination1)
    s3.upload_file(destination1, 'ece1779-bucket-1', filename1)
    os.remove(destination1)

    transformed2.save(filename=destination2)
    s3.upload_file(destination2, 'ece1779-bucket-1', filename2)
    os.remove(destination2)

    transformed3.save(filename=destination3)
    s3.upload_file(destination3, 'ece1779-bucket-1', filename3)
    os.remove(destination3)

    transformed4.save(filename=destination4)
    s3.upload_file(destination4, 'ece1779-bucket-1', filename4)
    os.remove(destination4)



@photos.route('/display')
@login_required
def display():
    user_name = current_user.username
    return user_name
