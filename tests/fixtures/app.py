from typing import Generator

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app


@pytest.fixture(autouse=True)
def app() -> Generator[Flask, None, None]:
    app = create_app()
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    ctx = app.app_context()
    ctx.push()

    yield app

    ctx.pop()


@pytest.fixture()
def client(app: Flask) -> FlaskClient:
    return app.test_client()
