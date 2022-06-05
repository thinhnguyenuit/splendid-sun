from app.models import User

EMAIL = "test@mail.com"
PASSWORD = "testpassword"
USERNAME = "test"

REGISTER_DATA = {
    "email": EMAIL,
    "username": USERNAME,
    "password": PASSWORD,
    "confirm_password": PASSWORD,
}

LOGIN_DATA = {"email": EMAIL, "password": PASSWORD}
LOGIN_DATA_INVALID = {"email": EMAIL, "password": None}

USER = User(id=1, email=EMAIL, username=USERNAME, password=PASSWORD)

REGISTER_DATA_INVALID = {
    "email": "a@email.com",
    "username": "z",
    "password": "z",
    "confirm_password": "zxzx",
}

LOGIN_DATA_INCORRECT_PASSWORD = {"email": EMAIL, "password": "1"}

UPDATED_USERNAME = f"{USERNAME}_UPDATED"
UPDATE_USER_DATA = {"email": f"UPDATED_{EMAIL}", "username": UPDATED_USERNAME}
UPDATE_USER_DATA_INVALID = {"email": EMAIL, "username": None}
