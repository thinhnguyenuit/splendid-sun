from typing import Optional
from app.extensions import db
from app.models import Comment


class CommentRepository:
    def __init__(self) -> None:
        self.db = db

    def get_all(self) -> Optional[Comment]:
        return Comment.query.all()

    def get_by_post_id(self, post_id: int) -> Optional[Comment]:
        return Comment.query.filter_by(post_id=post_id).all()

    def create(self, comment: Comment) -> None:
        self.db.session.add(comment)
        self.db.session.commit()
