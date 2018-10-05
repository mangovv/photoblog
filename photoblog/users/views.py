from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from photoblog import db
from photoblog.models import User
from photoblog.users.forms import LoginForm,RegistrationForm


users = Blueprint('users', __name__)
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


            return redirect(url_for('core.welcome'))
    return render_template('login.html', title=title,form=form)