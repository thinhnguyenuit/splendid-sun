import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from app.core.views import core
from app.extensions import db, login_manager
from app.users.views import users


def create_app() -> Flask:
    app = Flask(__name__)
    configure_app(app)
    configure_extensions(app)
    return app


def configure_app(app: Flask) -> None:
    load_dotenv()

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.register_blueprint(core)
    app.register_blueprint(users)


def configure_extensions(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "users.login"
