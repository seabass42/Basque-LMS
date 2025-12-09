import os

from flask import Flask
from flask_login import LoginManager

from .config import Config
from .models import db

login_manager = LoginManager()
login_manager.login_view = 'auth.login' 


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.main.routes import main
    from app.auth.routes import auth
    from app.instructor.routes import instructor  

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(instructor, url_prefix="/instructor")  

    with app.app_context():
        db.create_all()import os

from flask import Flask
from flask_login import LoginManager

from .config import Config
from .models import db

login_manager = LoginManager()
login_manager.login_view = 'auth.login' 


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    from app.main.routes import main
    from app.auth.routes import auth
    from app.instructor.routes import instructor  

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(instructor, url_prefix="/instructor")  

    with app.app_context():
        db.create_all()

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    return app


    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        from .models import User
        return User.query.get(int(user_id))

    return app
