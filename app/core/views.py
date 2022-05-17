from flask import Blueprint, render_template, request

from app.blog_posts.repositories import BlogPostRepository

core = Blueprint("core", __name__)
blog_post_repo = BlogPostRepository()


@core.route("/")
def index() -> str:
    page = request.args.get("page", 1, type=int)
    blog_posts = blog_post_repo.get_blog_posts_paginate(page_key=page)
    return render_template("index.html", blog_posts=blog_posts)


@core.route("/info")
def info() -> str:
    return render_template("info.html")


def get_default_blog_post_repo() -> BlogPostRepository:
    return BlogPostRepository()
