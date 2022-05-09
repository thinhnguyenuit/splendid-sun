from typing import Any

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from app.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def check_email(self, field: Any) -> None:
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email is already in use.")

    def check_username(self, field: Any) -> None:
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username is already in use.")


class UpdateUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    picture = FileField(
        "Update Profile Picture", validators=[FileAllowed(["jpg", "png", "jpeg"])]
    )
    submit = SubmitField("Update")

    def check_email(self, field: Any) -> None:
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")

    def check_username(self, field: Any) -> None:
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Sorry, that username is taken!")
