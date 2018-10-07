from flask import render_template, request, session, redirect, url_for, escape, Blueprint
from photoblog.models import Photo
from photoblog import db

display = Blueprint('view',__name__)

@display.route('/view')
def view():
    username_session="Anthony"
    #query = Photo.query.filter_by(title = 'yellow')
    url_list=[]
    a = Photo.query.with_entities(Photo.scale_down).first()[0]
    b = Photo.query.with_entities(Photo.enlarge).first()[0]
    c = Photo.query.with_entities(Photo.black_white).first()[0]

    url_list.append(a)
    url_list.append(b)
    url_list.append(c)
    return render_template("display.html", user_name=username_session, image_list=url_list)
