from flask import render_template, Blueprint
from photoblog.models import Photo
from flask_login import login_user, current_user, logout_user, login_required

display = Blueprint('view',__name__)

@display.route('/view/<title>')
@login_required
def view(title):

    url_list=[]
    a = Photo.query.filter_by(user_id=current_user.id).filter_by(title=title).with_entities(Photo.original).first()[0]
    b = Photo.query.filter_by(user_id=current_user.id).filter_by(title = title).with_entities(Photo.rotate).first()[0]
    c = Photo.query.filter_by(user_id=current_user.id).filter_by(title = title).with_entities(Photo.sepia).first()[0]
    d = Photo.query.filter_by(user_id=current_user.id).filter_by(title = title).with_entities(Photo.black_white).first()[0]

    url_list.append(a)
    url_list.append(b)
    url_list.append(c)
    url_list.append(d)

    return render_template("display.html", user_name=current_user.username, image_list=url_list)

@display.route('/home_page')
@login_required
#welcome when log in successfully
def home_page():
    title = 'welcome'
    url_list=[]
    tit_list=[]
    address_list = Photo.query.filter_by(user_id = current_user.id).with_entities(Photo.thumbnail).all()
    for address in address_list:
        url_list.append(address[0])

    title_list = Photo.query.filter_by(user_id = current_user.id).with_entities(Photo.title).all()
    for title in title_list:
        tit_list.append(title)

    return render_template('home_page.html', user_name=current_user.username ,title_list = tit_list, image_list=url_list)
