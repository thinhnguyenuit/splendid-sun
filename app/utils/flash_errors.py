from flask import flash
from flask_wtf import FlaskForm


def flash_errors(form: FlaskForm) -> None:
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"{error}")
