from photoblog import app as application
from photoblog.models import db


if __name__ == '__main__':
    #first run this proj -->you need to create all the tables
    #db.drop_all()
    #db.create_all()
    application.run(debug=True)
