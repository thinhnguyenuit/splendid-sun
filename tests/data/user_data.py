from app.models import User

EMAIL = "test@mail.com"
PASSWORD = "test"
USERNAME = "test"

REGISTER_DATA = {
    "email": EMAIL,
    "username": USERNAME,
    "password": PASSWORD,
    "confirm_password": PASSWORD,
}

LOGIN_DATA = {"email": EMAIL, "password": PASSWORD}

USER = User(email=EMAIL, username=USERNAME, password=PASSWORD)
