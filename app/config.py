import os

basedir = os.path.abspath(os.path.dirname(__file__))

clas Config:
    SECRET_KEY = "Basque123"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
