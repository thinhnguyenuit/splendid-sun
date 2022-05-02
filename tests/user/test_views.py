from unittest import mock

from flask_login import login_user
from werkzeug.test import Client

from app.users import views
from tests.data import user_data


class TestUserView:
    def test_register_user(self, client: Client) -> None:
        with mock.patch.object(views, "user_repo") as mock_repo:
            mock_repo.add.return_value = None
            response = client.post(
                "/register", data=user_data.REGISTER_DATA, follow_redirects=True
            )

        assert len(response.history) == 1
        assert response.request.path == "/login"

    def test_login_user(self, client: Client) -> None:
        with mock.patch.object(views, "user_repo") as mock_repo:
            mock_repo.get_user_by_email.return_value = user_data.USER
            response = client.post(
                "/login", data=user_data.LOGIN_DATA, follow_redirects=False
            )

        assert response.request.path == "/login"
