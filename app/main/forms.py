from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, \
    HiddenField, RadioField, FileField, SubmitField, IntegerField

from  wtforms.validators import Required, Length, Email, Regexp


class NameForm(FlaskForm):
    name = StringField()