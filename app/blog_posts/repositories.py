from typing import List

from app.extensions import db
from app.models import BlogPost


class BlogPostRepository(object):
    def __init__(self) -> None:
        self.db = db

    def get_blog_posts(self) -> List[BlogPost]:
        return BlogPost.query.all()

    def get_blog_posts_paginate(
        self, page_key: int, page_size: int = 10
    ) -> List[BlogPost]:
        return BlogPost.query.order_by(BlogPost.created_at.desc()).paginate(
            page=page_key, per_page=page_size
        )
