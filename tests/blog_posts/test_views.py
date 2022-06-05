from unittest import mock

from mock import MagicMock

from tests import factories
from tests.base import AppBaseTestCase
from tests.data import posts_data


class TestBlogPostsView(AppBaseTestCase):
    @mock.patch("flask_login.utils._get_user")
    def test_create_post(self, current_user: MagicMock) -> None:
        current_user.return_value = factories.UserFactory()
        response = self.client.post(
            "/create", data=posts_data.CREATE_POST_DATA, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/"

    @mock.patch("flask_login.utils._get_user")
    def test_create_post_invalid_form(self, curr_user: MagicMock) -> None:
        curr_user.return_value = factories.UserFactory()
        response = self.client.post(
            "/create", data=posts_data.CREATE_POST_DATA_INVALID, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/create"

    def test_get_blog_post(self) -> None:
        user = factories.UserFactory()
        self.db.session.add(user)
        post = factories.BlogPostFactory(user_id=user.id)
        self.db.session.add(post)
        self.db.session.commit()

        response = self.client.get(f"/{post.id}")

        assert response.status_code == 200
