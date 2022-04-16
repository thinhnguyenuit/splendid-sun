from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email, EqualTo

from splendidsuns.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Corfirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def check_email(self, field) -> None:
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Email is already in use.")

    def check_username(self, field) -> None:
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Username is already in use.")
