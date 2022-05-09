from typing import Union

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.wrappers.response import Response

from app.blog_posts.repositories import BlogPostRepository
from app.models import User
from app.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from app.users.image_handler import add_profile_image
from app.users.repositories import UserRepository

users = Blueprint("users", __name__)
user_repo = UserRepository()
blog_post = BlogPostRepository()


@users.route("/register", methods=["GET", "POST"])
def register() -> Union[str, Response]:
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        )

        user_repo.add(user)
        flash("Registration is complete. Now you can login.")
        return redirect(url_for("users.login"))
    if form.errors.items():
        for field_name, error in form.errors.items():
            flash(f"{field_name}: {error}")
    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    form = LoginForm()

    if form.validate_on_submit():
        user = user_repo.get_user_by_email(form.email.data)

        if user is None:
            flash("Could not find user with that email.")
        elif not user.check_password(form.password.data):
            flash("Incorrect password.")
        else:
            login_user(user)
            flash(f"Login is complete. Welcome back {user.username}!")

            next_page = request.args.get("next")

            if next_page is None or next_page[0] != "/":
                next_page = url_for("core.index")

            return redirect(next_page)
    if form.errors.items():
        for field_name, error in form.errors.items():
            flash(f"{field_name}: {error}")
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
            username = current_user.username
            img = add_profile_image(form.picture.data, username)
            current_user.profile_image = img

        current_user.username = form.username.data
        current_user.email = form.email.data
        user_repo.update_user(current_user)
        flash("User Updated")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    else:
        flash("Error updating user")
        form.username.data = current_user.username
        form.email.data = current_user.email
    profile_image = url_for(
        "static", filename=f"profile_imgs{current_user.profile_image}"
    )
    if form.errors.items():
        for field_name, error in form.errors.items():
            flash(f"{field_name}: {error}")
    return render_template("account.html", profile_image=profile_image, form=form)


@users.route("/<username>")
def user_posts(username: str) -> str:
    page = request.args.get("page", 1, type=int)
    user = user_repo.get_user_by_username(username)
    blog_posts = blog_post.get_blog_posts_by_user(user, page_key=page)
    return render_template("user_blog_posts.html", blog_posts=blog_posts, user=user)
