from typing import Union

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.wrappers.response import Response

from app.extensions import db
from app.models import User
from app.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from app.users.image_handler import add_profile_image

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register() -> Union[str, Response]:
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )

        db.session.add(user)
        db.session.commit()
        flash("Registration is complete. Now you can login.")
        return redirect(url_for("users.login"))
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash(f"Login is complete. Welcome back {user.username}!")

            next_page = request.args.get("next")

            if next_page is None or next_page[0] != "/":
                next_page = url_for("core.index")

            return redirect(next_page)
        else:
            flash("Email or pasword is not correct.")
    return render_template("login.html", form=form)


@users.route("/logout")
def logout() -> Response:
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("core.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account() -> Union[str, Response]:

    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.data
            img = add_profile_image(form.picture, username)
            current_user.profile_image = img

        current_user.username = form.username.data
        current_user.email = form.username.data
        db.session.commit()
        flash("User Updated")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for(
        "static", filename=f"profile_imgs{current_user.profile_image}"
    )

    return render_template("account.html", profile_image=profile_image, form=form)
