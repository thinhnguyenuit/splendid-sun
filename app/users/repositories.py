from typing import Optional

from app.extensions import db
from app.models import User


class UserRepository(object):
    def __init__(self) -> None:
        self.db = db

    def add(self, user: User) -> None:
        self.db.session.add(user)
        self.db.session.commit()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).one_or_none()

    def update_user(self, user: User) -> None:
        self.db.session.merge(user)
        self.db.session.commit()
