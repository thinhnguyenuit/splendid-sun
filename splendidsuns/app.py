import os

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from splendidsuns.extensions import db, login_manager


def create_app() -> Flask:
    app = Flask("splendidsunsets")
    configure_app(app)
    configure_extensions(app)
    return app


def configure_app(app: Flask) -> None:
    if os.getenv("USE_DOTENV", default="false") == "true":
        load_dotenv()

    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def configure_extensions(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "users.login"
