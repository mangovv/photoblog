from flask import render_template,Blueprint


core = Blueprint('core',__name__)

@core.route('/')
def index():
#This is the home page view.

    title = "PhotoBLog"

    return render_template('index.html',title = title)

@core.route('/home_page')
#welcome when log in successfully
def welcome():
    title = 'welcome'
    return render_template('home_page.html',title = title)
