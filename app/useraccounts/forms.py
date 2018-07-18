#!usr/bin/env/ python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, \
    HiddenField, RadioField, FileField, SubmitField, IntegerField

from  wtforms.validators import Required, Length, Email, Regexp,DataRequired
from . import models


class LoginForm(FlaskForm):
    Username = StringField()
    Password = PasswordField()
    remember_me = BooleanField(label='Keep me logged in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), len(1, 60), Email()])