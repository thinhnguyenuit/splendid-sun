from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from splendidsuns.extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(256), unique=True, index=True)
    password = db.Column(db.String(128))
    profile_image = db.Column(
        db.String(64), nullable=False, default="default_profile.png"
    )

    def __init__(self, username, email, password) -> None:
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_user(user_id) -> User:
    return User.query.get(user_id)
