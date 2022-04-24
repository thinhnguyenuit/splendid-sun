from app.blog_posts.forms import BlogPostForm
from flask import Blueprint, flash, redirect, render_template, request, url_for, abort
from flask_login import login_required, current_user
from app.models import BlogPost
from app.extensions import db
from typing import Union
from werkzeug.wrappers.response import Response

blog_posts = Blueprint("blog_posts", __name__)


@blog_posts.route("/create", methods=["GET", "POST"])
@login_required
def create_post() -> Union[str, Response]:
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(blog_post)
        db.session.commit()
        flash("Blog Post Created")
        return redirect(url_for("core.index"))

    return render_template("create_post.html", form=form)


@blog_posts.route("/<int:blog_post_id>")
def blog_post(blog_post_id: int) -> str:
    post = BlogPost.query.get_or_404(blog_post_id)
    return render_template("blog_post.html", post=post)


@blog_posts.route("/<int:blog_post_id>/update", methods=["GET", "POST"])
@login_required
def update(blog_post_id: int) -> Union[str, Response]:
    post = BlogPost.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Post Updated")
        return redirect(url_for("blog_posts.blog_post", blog_post_id=post.id))

    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title="Update", form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=["POST"])
@login_required
def delete_post(blog_post_id: int) -> Response:
    post = BlogPost.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()
    flash("Post Deleted")
    return redirect(url_for("core.index"))
