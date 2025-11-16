from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

# find the working directory you are in
basedir =  os.path.abspath(os.path.dirname(__file__))
def create_app():

    myapp_obj = Flask(__name__)
    myapp_obj.config.from_object(Config)

    db.init_app(myapp_obj)
    with myapp_obj.app_context():
        from . import routes
        db.create_all()

    return myapp_obj
