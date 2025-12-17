import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .config import Config
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    from app.models import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
        
    from app.main.routes import main
    from app.auth.routes import auth
    from app.instructor.routes import instructor
    from app.student.routes import student

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(instructor, url_prefix="/instructor")
    app.register_blueprint(student, url_prefix="/student")

    with app.app_context():
        db.create_all()
    return app
