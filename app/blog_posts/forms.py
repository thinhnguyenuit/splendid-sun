from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired(), Length(min=1, max=128)])
    content = TextAreaField("Content", validators=[DataRequired(), Length(min=1)])
    submit = SubmitField("Post")
