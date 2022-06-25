from typing import Union

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from werkzeug.wrappers.response import Response

from app.blog_posts.forms import BlogPostForm
from app.blog_posts.repositories import BlogPostRepository
from app.models import BlogPost
from app.utils.flash_errors import flash_errors
from app.models import Comment
from app.comments.forms import CommentForm
from app.comments.repositories import CommentRepository

blog_posts = Blueprint("blog_posts", __name__)
blog_post_repo = BlogPostRepository()
comment_repo = CommentRepository()


@blog_posts.route("/create", methods=["GET", "POST"])
@login_required
def create_post() -> Union[str, Response]:
    form = BlogPostForm()

    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            content=form.content.data,
            user_id=current_user.id,
            user=current_user,
        )
        blog_post_repo.create_blog_post(post)
        flash("Blog Post Created")
        return redirect(url_for("core.index"))
    else:
        flash_errors(form)
    return render_template("create_post.html", form=form)


@blog_posts.route("/<int:blog_post_id>", methods=["GET", "POST"])
def blog_post(blog_post_id: int) -> str:
    post = blog_post_repo.get_blog_post_by_id(blog_post_id)
    comments = comment_repo.get_by_post_id(blog_post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            post_id=blog_post_id,
        )
        comment_repo.create(comment)
        flash("Comment Created")
    else:
        flash_errors(form)
    return render_template("blog_post.html", post=post, comments=comments, form=form)


@blog_posts.route("/<int:blog_post_id>/update", methods=["GET", "POST"])
@login_required
def update(blog_post_id: int) -> Union[str, Response]:
    post = blog_post_repo.get_blog_post_by_id(blog_post_id)

    if post.author != current_user:
        abort(403)

    form = BlogPostForm()

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        blog_post_repo.update_blog_post(post)
        flash("Post Updated")
        return redirect(url_for("blog_posts.blog_post", blog_post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    else:
        flash_errors(form)

    return render_template("create_post.html", title="Update", form=form)


@blog_posts.route("/<int:blog_post_id>/delete", methods=["POST"])
@login_required
def delete_post(blog_post_id: int) -> Response:
    post = BlogPost.query.get_or_404(blog_post_id)

    if post.author != current_user:
        abort(403)

    blog_post_repo.delete_blog_post(post)

    flash("Post Deleted")
    return redirect(url_for("core.index"))
