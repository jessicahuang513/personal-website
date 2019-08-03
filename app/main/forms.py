from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, \
    TextAreaField, SelectField, IntegerField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, \
    Length, NumberRange
from app.models import User, Post

class AddPostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Length(min=0, max=1000)])
    body = TextAreaField('Post', validators=[Length(min=0, max=10000)])
    submit = SubmitField('Submit')