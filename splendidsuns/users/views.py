from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

from splendidsuns.extensions import db
from splendidsuns.models import User
from splendidsuns.users.forms import LoginForm, RegistrationForm

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register() -> str:
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
def login() -> str:
    form = LoginForm()

    if LoginForm.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash(f"Login is complete. Welcome back {user.username}!")

            next_page = request.args.get("next")

            if next_page is None or next_page[0] != "/":
                next_page = url_for("core.index")

            return redirect(next_page)
        return render_template("login.html", form=form)


@users.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("core.index"))
