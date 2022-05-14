from typing import Generator
from unittest import mock
from unittest.mock import MagicMock

import flask
import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.users import views as user_views
from app.blog_posts import views as blog_views
from app.core import views as core_views


@pytest.fixture(autouse=True)
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["LOGIN_DISABLED"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = ""
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()


@pytest.fixture()
def mock_user_repo() -> Generator[MagicMock, None, None]:
    with mock.patch.object(user_views, "user_repo") as mock_repo:
        yield mock_repo


@pytest.fixture()
def mock_curr_user() -> Generator[MagicMock, None, None]:
    with mock.patch.object(user_views, "current_user") as mock_user:
        yield mock_user


@pytest.fixture()
def mock_render_template() -> Generator[MagicMock, None, None]:
    with mock.patch.object(flask, "render_template") as mock_render_template:
        yield mock_render_template


@pytest.fixture()
def mock_user_blog_repo() -> Generator[MagicMock, None, None]:
    with mock.patch.object(user_views, "blog_post") as mock_repo:
        yield mock_repo


@pytest.fixture()
def mock_blog_post_repo() -> Generator[MagicMock, None, None]:
    with mock.patch.object(blog_views, "blog_post_repo") as mock_repo:
        yield mock_repo


@pytest.fixture()
def mock_core_blog_repo() -> Generator[MagicMock, None, None]:
    with mock.patch.object(core_views, "blog_post_repo") as mock_repo:
        yield mock_repo
