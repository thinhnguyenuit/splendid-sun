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

REGISTER_DATA_INVALID = {
    "email": "a@email.com",
    "username": "z",
    "password": "z",
    "confirm_password": "zxzx",
}

LOGIN_DATA_INCORRECT_PASSWORD = {"email": EMAIL, "password": "1"}

UPDATE_USER_DATA = {"email": EMAIL, "username": f"{USERNAME}_UPDATED"}
