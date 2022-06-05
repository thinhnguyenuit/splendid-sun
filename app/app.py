import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask
from flask_migrate import Migrate

from app.blog_posts.views import blog_posts
from app.core.views import core
from app.error_pages.views import error_pages
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
    uri = os.environ.get("DATABASE_URL")
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=5)

    app.register_blueprint(core)
    app.register_blueprint(users)
    app.register_blueprint(blog_posts)
    app.register_blueprint(error_pages)


def configure_extensions(app: Flask) -> None:
    db.init_app(app)
    Migrate(app, db)

    login_manager.init_app(app)
    login_manager.login_view = "users.login"
