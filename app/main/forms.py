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


class CommentForm(FlaskForm):
    email = StringField('* Email', validators=[DataRequired(), Length(1, 128), Email()])
    author = StringField('* Name', validators=[DataRequired(), Length(1, 200)])
    body = TextAreaField('* Comment <small><span class="label label-info">markdown</span></small>',
                         validators=[DataRequired()])
    comment_id = HiddenField('comment_id')

