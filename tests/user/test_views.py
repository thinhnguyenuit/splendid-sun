import re
from unittest import mock
from unittest.mock import MagicMock

from flask.testing import FlaskClient

from app.users import views
from tests.data import posts_data, user_data


class TestUserView:
    def test_register_user(
        self, client: FlaskClient, mock_user_repo: MagicMock
    ) -> None:
        mock_user_repo.add.return_value = None
        response = client.post(
            "/register", data=user_data.REGISTER_DATA, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/login"

    def test_register_user_invalid_data(
        self, client: FlaskClient, mock_user_repo: MagicMock
    ) -> None:
        mock_user_repo.add.return_value = None
        response = client.post(
            "/register", data=user_data.REGISTER_DATA_INVALID, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/register"

    def test_login_user(self, client: FlaskClient, mock_user_repo: MagicMock) -> None:
        mock_user_repo.get_user_by_email.return_value = user_data.USER
        response = client.post(
            "/login", data=user_data.LOGIN_DATA, follow_redirects=False
        )

        assert response.status_code == 302
        mock_user_repo.get_user_by_email.assert_called()
        assert response.request.path == "/login"

    def test_login_user_not_exist(
        self, client: FlaskClient, mock_user_repo: MagicMock
    ) -> None:
        mock_user_repo.get_user_by_email.return_value = None

        response = client.post(
            "/login", data=user_data.LOGIN_DATA, follow_redirects=False
        )

        assert (
            re.search(
                "Could not find user with that email.", response.get_data(as_text=True)
            )
            is not None
        )
        assert response.status_code == 200
        mock_user_repo.get_user_by_email.assert_called()
        assert response.request.path == "/login"

    def test_login_user_incorrct_password(
        self, client: FlaskClient, mock_user_repo: MagicMock
    ) -> None:
        mock_user_repo.get_user_by_email.return_value = user_data.USER

        response = client.post(
            "/login",
            data=user_data.LOGIN_DATA_INCORRECT_PASSWORD,
            follow_redirects=False,
        )

        assert (
            re.search("Incorrect password.", response.get_data(as_text=True))
            is not None
        )
        assert response.status_code == 200
        mock_user_repo.get_user_by_email.assert_called()
        assert response.request.path == "/login"

    def test_login_user_invalid_form(self, client: FlaskClient) -> None:
        response = client.post(
            "/login", data=user_data.LOGIN_DATA_INVALID, follow_redirects=False
        )

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/login"

    def test_logout_user(
        self, client: FlaskClient, mock_core_blog_repo: MagicMock
    ) -> None:
        mock_core_blog_repo.get_blog_posts_paginate.return_value = (
            posts_data.PAGINATED_BLOG_POSTS
        )

        response = client.get("/logout", follow_redirects=True)

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/"

    def test_update_user(
        self, client: FlaskClient, mock_user_repo: MagicMock, mock_curr_user: MagicMock
    ) -> None:
        mock_user_repo.update_user.return_value = None
        response = client.post(
            "/account", data=user_data.UPDATE_USER_DATA, follow_redirects=False
        )

        assert response.status_code == 302
        assert len(response.history) == 0
        assert response.request.path == "/account"

    def test_update_user_get(
        self, client: FlaskClient, mock_user_repo: MagicMock, mock_curr_user: MagicMock
    ) -> None:

        with mock.patch.object(views, "render_template") as mock_render_template:
            mock_render_template.return_value = ""
            response = client.get("/account", follow_redirects=False)

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/account"

    def test_update_user_invalid_form(
        self, client: FlaskClient, mock_curr_user: MagicMock
    ) -> None:
        with mock.patch.object(views, "render_template") as mock_render_template:
            mock_render_template.return_value = ""
            response = client.post(
                "/account",
                data=user_data.UPDATE_USER_DATA_INVALID,
                follow_redirects=False,
            )

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/account"

    def test_get_user_post(
        self,
        client: FlaskClient,
        mock_user_repo: MagicMock,
        mock_user_blog_repo: MagicMock,
        mock_render_template: MagicMock,
    ) -> None:
        mock_user_repo.get_user_by_id.return_value = user_data.USER
        mock_user_blog_repo.get_blog_posts_by_user.return_value = (
            posts_data.PAGINATED_BLOG_POSTS
        )
        mock_render_template.return_value = ""

        response = client.get(f"/{user_data.USER.username}")

        assert response.status_code == 200
