import re
from unittest import mock
from unittest.mock import MagicMock

from tests import factories
from tests.base import AppBaseTestCase
from tests.data import user_data


class TestUserViews(AppBaseTestCase):
    def test_register_user(self) -> None:
        response = self.client.post(
            "/register", data=user_data.REGISTER_DATA, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/login"

    def test_register_user_invalid_data(self) -> None:
        response = self.client.post(
            "/register", data=user_data.REGISTER_DATA_INVALID, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/register"

    def test_login_user(self) -> None:
        user = factories.UserFactory()
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client.post(
            "/login",
            data={"email": user.email, "password": "testpassword"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/"

    def test_login_user_not_exist(self) -> None:
        response = self.client.post(
            "/login", data=user_data.LOGIN_DATA, follow_redirects=True
        )

        assert (
            re.search(
                "Could not find user with that email.", response.get_data(as_text=True)
            )
            is not None
        )
        assert response.status_code == 200
        assert response.request.path == "/login"

    def test_login_user_incorrct_password(self) -> None:
        user = factories.UserFactory()
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client.post(
            "/login",
            data=user_data.LOGIN_DATA_INCORRECT_PASSWORD,
            follow_redirects=False,
        )

        assert response.status_code == 200
        assert response.request.path == "/login"

    def test_login_user_invalid_form(self) -> None:
        response = self.client.post(
            "/login", data=user_data.LOGIN_DATA_INVALID, follow_redirects=True
        )

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/login"

    def test_logout_user(self) -> None:
        response = self.client.get("/logout", follow_redirects=True)

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == "/"

    @mock.patch("flask_login.utils._get_user")
    def test_update_user(self, current_user: MagicMock) -> None:
        user = factories.UserFactory()
        self.db.session.add(user)
        self.db.session.commit()

        current_user.return_value = user

        response = self.client.post(
            "/edit_profile",
            data={"email": f"new-{user.email}", "username": f"new_{user.username}"},
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert len(response.history) == 1
        assert response.request.path == f"/users/{user.username}"

    @mock.patch("flask_login.utils._get_user")
    def test_update_user_get(self, current_user: MagicMock) -> None:
        current_user.return_value = factories.UserFactory()
        response = self.client.get("/edit_profile", follow_redirects=True)

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/edit_profile"

    @mock.patch("flask_login.utils._get_user")
    def test_update_user_invalid_form(self, current_user: MagicMock) -> None:
        current_user.return_value = factories.UserFactory()
        response = self.client.post(
            "/edit_profile",
            data=user_data.UPDATE_USER_DATA_INVALID,
            follow_redirects=True,
        )

        assert response.status_code == 200
        assert len(response.history) == 0
        assert response.request.path == "/edit_profile"

    def test_get_user_profile(self) -> None:
        user = factories.UserFactory()
        self.db.session.add(user)
        self.db.session.commit()

        response = self.client.get(f"/users/{user.username}")

        assert response.status_code == 200
