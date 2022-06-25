from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=1)])
    submit = SubmitField("Submit")
