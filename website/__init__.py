from flask import Flask
from .views import views
from .api import api_bp
from .auth import auth
from flask_sqlalchemy import SQLAlchemy
from os import path
from .models import db
from flask_login import LoginManager

DB_NAME = 'database.db'

def create_app():
    app = Flask(__name__)

    app.secret_key = 'akfmapodjfmlawsmdpisajd'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")
    app.register_blueprint(api_bp, url_prefix="/api")

    from .models import User, Note

    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
