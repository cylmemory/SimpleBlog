#!usr/bin/env/ python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, \
    HiddenField, RadioField, FileField, SubmitField, IntegerField, SelectField, ValidationError

from  wtforms.validators import Required, Length, Email, Regexp, DataRequired, EqualTo
from .models import User, ROLES


class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    remember_me = BooleanField(label='Keep me logged in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 60), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 60),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'username must have only letters, numbers dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])


    def validate_email(self, field):
        if User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('Username has exist')


class UserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 125), Email()])
    role = SelectField('Role', choices=ROLES)
