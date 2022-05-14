from unittest import mock

from flask.testing import FlaskClient
from mock import MagicMock

from app.blog_posts import views
from tests.data import posts_data, user_data


class TestBlogPostsView:
    def test_create_post(
        self,
        client: FlaskClient,
        mock_blog_post_repo: MagicMock,
        mock_core_blog_repo: MagicMock,
        mock_post_user: MagicMock,
    ) -> None:
        mock_blog_post_repo.create_blog_post.return_value = None
        mock_core_blog_repo.get_blog_posts_paginate.return_value = (
            posts_data.PAGINATED_BLOG_POSTS
        )
        mock_post_user.return_value = None
        response = client.post(
            "/create", data=posts_data.CREATE_POST_DATA, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/"
        mock_blog_post_repo.create_blog_post.assert_called()

    def test_create_post_invalid_form(
        self, client: FlaskClient, mock_curr_user: MagicMock
    ) -> None:
        response = client.post(
            "/create", data=posts_data.CREATE_POST_DATA_INVALID, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/create"

    def test_get_blog_post(
        self, client: FlaskClient, mock_blog_post_repo: MagicMock
    ) -> None:
        mock_blog_post_repo.get_blog_post_by_id.return_value = posts_data.BLOG_POST
        with mock.patch.object(views, "render_template") as mock_render_template:
            mock_render_template.return_value = ""
            response = client.get("/1")

        assert response.status_code == 200
        mock_blog_post_repo.get_blog_post_by_id.assert_called()
