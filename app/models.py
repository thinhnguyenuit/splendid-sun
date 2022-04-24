from __future__ import annotations
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.extensions import db, login_manager


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(256), unique=True, index=True)
    password = db.Column(db.String(128))
    profile_image = db.Column(
        db.String(64), nullable=False, default="default_profile.jpg"
    )

    posts = db.relationship("BlogPost", backref="author", lazy=True)

    def __init__(self, username: str, email: str, password: str) -> None:
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f"User('{self.username}', '{self.email}')"


@login_manager.user_loader
def load_user(user_id: int) -> User:
    return User.query.get(user_id)


class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    user = db.relationship(User)

    def __init__(self, title: str, content: str, user_id: int) -> None:
        self.title = title
        self.content = content
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"Post id: {self.id}, title: {self.title}, user_id: {self.user_id}"
