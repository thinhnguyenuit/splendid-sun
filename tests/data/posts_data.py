from datetime import datetime

from flask_sqlalchemy import Pagination
from mock import MagicMock

from app.models import BlogPost
from tests.data.user_data import USER

PAGINATED_BLOG_POSTS = Pagination(None, 1, 1, 1, [])

CREATE_POST_DATA = {
    "title": "Test Title",
    "content": "Test Content",
}

CREATE_POST_DATA_INVALID = {
    "title": "",
    "content": None,
}

BLOG_POST = BlogPost(user_id=1, title="Test Title", content="Test Content")
BLOG_POST.created_at = datetime.now()
BLOG_POST.updated_at = datetime.now()

UPDATE_POST_DATA = {
    "title": "Test Title",
    "content": "Test Content Updated",
}
