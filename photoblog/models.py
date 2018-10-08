import pymysql
from photoblog import db
from werkzeug.security import generate_password_hash,check_password_hash
from datetime import datetime
from flask_login import UserMixin
from photoblog import login_manager

# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model,UserMixin):
    _tablename_="user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects Photos to a User Author.
    # ONE To Many  User to Many Photos
    photo = db.relationship('Photo',backref='author',lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.email = email

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"

class Photo(db.Model):
    _tablename_='photo'
    # Setup the relationship to the User table
    users = db.relationship(User)
    photo_id = db.Column(db.Integer, primary_key=True, autoincrement= True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    thumbnail = db.Column(db.String(200), nullable=False)
    rotate = db.Column(db.String(200), nullable=False)
    sepia = db.Column(db.String(200), nullable=False)
    black_white = db.Column(db.String(200), nullable=False)


    def __init__(self, title, user_id, thumbnail, rotate, sepia, black_white):
        self.title = title
        self.user_id = user_id
        self.thumbnail = thumbnail
        self.rotate = rotate
        self.sepia = sepia
        self.black_white = black_white

    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"





