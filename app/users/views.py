from typing import Union

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, abort
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.wrappers.response import Response

from app.blog_posts.repositories import BlogPostRepository
from app.models import User
from app.users.forms import LoginForm, RegistrationForm, UpdateUserForm
from app.users.image_handler import add_profile_image
from app.users.repositories import UserRepository
from app.utils.flash_errors import flash_errors

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
        flash("Registration successful. Now you can login.")
        return redirect(url_for("users.login"))
    else:
        flash_errors(form)
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
            session.permanent = True
            flash(f"Login successful. Welcome back {user.username}!")

            next_page = request.args.get("next")

            if next_page is None or next_page[0] != "/":
                next_page = url_for("core.index")

            return redirect(next_page)
    else:
        flash_errors(form)
    return render_template("login.html", form=form)


@users.route("/logout")
def logout() -> Response:
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for("core.index"))


@users.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile() -> Union[str, Response]:

    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            img = add_profile_image(form.picture.data, username)
            current_user.profile_image = img

        if current_user.username != form.username.data and user_repo.get_user_by_username(form.username.data):
            flash("Username already taken.")
            return render_template("edit_profile.html", form=form)

        if current_user.email != form.email.data and user_repo.get_user_by_email(form.email.data):
            flash("Email already taken.")
            return render_template("edit_profile.html", form=form)

        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        user_repo.update_user(current_user)
        flash("Your profile has been updated.")
        return redirect(url_for("users.user", username=current_user.username))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    else:
        flash("Error while updating profile.")
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
        flash(form.errors)
    return render_template("edit_profile.html", form=form)


@users.route("/users/<username>")
def user(username: str) -> str:
    page = request.args.get("page", 1, type=int)
    curr_user = user_repo.get_user_by_username(username)
    if not curr_user:
        abort(404)
    blog_posts = blog_post.get_blog_posts_by_user(curr_user, page_key=page)
    profile_image = url_for("static", filename=f"profile_imgs{curr_user.profile_image}")
    return render_template(
        "account.html",
        blog_posts=blog_posts,
        user=curr_user,
        profile_image=profile_image,
    )
