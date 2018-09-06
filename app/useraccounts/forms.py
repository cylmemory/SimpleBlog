#!usr/bin/env/ python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, TextAreaField, \
    HiddenField, RadioField, FileField, SubmitField, IntegerField, SelectField, ValidationError

from  wtforms.validators import  Length, Email, Regexp, DataRequired, EqualTo, URL, Optional
from .models import User, ROLES
from flask_login import current_user


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


class AddUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 60), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 60),
        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'username must have only letters, numbers dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2', message='password must match')])
    password2 = PasswordField('Confirm password', validators=[DataRequired()])
    role = SelectField('Role', choices=ROLES, default='reader')

    def validate_email(self, field):
        if User.objects.filter(email=field.data).count() > 0:
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.objects.filter(username=field.data).count() > 0:
            raise ValidationError('Username has exist')


class UpdateProfileForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 125), Email()])
    about_me = StringField('About_me')
    homepage_url = StringField('Homepage', validators=[URL(), Optional()])
    github = StringField('Github', validators=[URL(), Optional()])
    facebook = StringField('Facebook', validators=[URL(), Optional()])
    twitter = StringField('Twitter', validators=[URL(), Optional()])
    wechat = StringField('Wehcat', validators=[URL(), Optional()])
    weibo = StringField('Weibo', validators=[URL(), Optional()])


class ModifyPasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='password must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])

    def validate_current_password(self, field):
        if not current_user.verify_password(field.data):
            raise ValidationError('Current password is wrong')


class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 125), Email()])


class ResetPasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired(), EqualTo('confirm_password', message='password must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])