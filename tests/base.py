import unittest

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import create_app, extensions


def clean_db(db: SQLAlchemy) -> None:
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())


class AppBaseTestCase(unittest.TestCase):
    db: SQLAlchemy = None
    app: Flask = None  # type: ignore

    @classmethod
    def setUpClass(cls) -> None:
        super(AppBaseTestCase, cls).setUpClass()
        cls.app = create_app()
        cls.app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = "postgresql://postgres:postgres@localhost:5442/test_db"

        cls.db = extensions.db
        cls.db.app = cls.app
        cls.db.create_all()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.db.drop_all()
        super(AppBaseTestCase, cls).tearDownClass()

    def setUp(self) -> None:
        super(AppBaseTestCase, self).setUp()

        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.app.config["LOGIN_DISABLED"] = True

        self.client = self.app.test_client()
        self.db.create_all()

        self.app_context = self.app.app_context()
        self.app_context.push()

        clean_db(self.db)

    def tearDown(self) -> None:
        self.db.session.expunge_all()
        self.db.session.rollback()
        self.app_context.pop()

        super(AppBaseTestCase, self).tearDown()
