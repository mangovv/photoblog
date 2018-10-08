from flask import render_template, Blueprint
from photoblog.models import Photo
from flask_login import login_user, current_user, logout_user, login_required, login_manager

display = Blueprint('view',__name__)

@display.route('/view')
@login_required
def view():
    username_session=current_user.username
    query = Photo.query.filter_by(user_id = current_user.id)
    url_list=[]
    a = Photo.query.with_entities(Photo.rotate).first()[0]
    b = Photo.query.with_entities(Photo.sepia).first()[0]
    c = Photo.query.with_entities(Photo.black_white).first()[0]

    url_list.append(a)
    url_list.append(b)
    url_list.append(c)
    return render_template("display.html", user_name=username_session, image_list=url_list)

@display.route('/home_page')
#welcome when log in successfully
def welcome():
    title = 'welcome'
    return render_template('home_page.html',title = title)
