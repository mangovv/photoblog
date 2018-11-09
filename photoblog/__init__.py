from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)

#############################################################################
############ CONFIGURATIONS (CAN BE SEPARATE CONFIG.PY FILE) ###############
###########################################################################

app.config['SECRET_KEY'] = '123'


#################################
### DATABASE SETUPS ############
###############################
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:ece1779pass@107.22.38.176:3306/ece1779'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)
Migrate(app,db)
###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"


###########################
#### BLUEPRINT CONFIGS #######
#########################

from photoblog.users.user_util import users
#from photoblog.core.views import core
from photoblog.photos.upload import photos
from photoblog.photos.view import display
#db.create_all()


app.register_blueprint(users)
#app.register_blueprint(core)
app.register_blueprint(photos)
app.register_blueprint(display)

