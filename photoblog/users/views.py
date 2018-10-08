from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required, login_manager
from photoblog import db
from photoblog.models import User
from photoblog.users.forms import LoginForm,RegistrationForm

#from photoblog.models import load_user


users = Blueprint('users', __name__)

@users.route('/')
def index():
#This is the home page view.

    title = "PhotoBLog"

    return render_template('index.html',title = title)

@users.route('/home_page')
#welcome when log in successfully
def welcome():
    title = 'welcome'
    return render_template('home_page.html',title = title)

@users.route('/register', methods=['GET', 'POST'])
def register():
    title = 'resigter'
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('users.login'))
    return render_template('register.html', title =title, form=form)


@users.route('/login', methods=['GET', 'POST'])
def login():
    title = 'login'

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()

        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            # Log in the user

            login_user(user)
            flash('Logged in successfully.')


            return redirect(url_for('users.welcome'))
    return render_template('login.html', title=title,form=form)

@users.route('/logout')
@login_required
def logout():
    logout_user()
    return "Logged Out"



@users.route('/test', methods=['GET', 'POST'])
@login_required
def test():
    return 'test'