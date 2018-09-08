#!usr/bin/env/ python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, \
    HiddenField, RadioField, FileField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, Email, Regexp

from . import models


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    category = StringField('Category')
    tags = StringField('Tags')
    abstract = TextAreaField('Abstract')
    content = TextAreaField('Content')
    status = HiddenField('status')
    post_id = HiddenField('post_id')

