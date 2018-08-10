#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect, render_template, url_for, request, g, flash, session, current_app, abort
from .models import User
from .forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime
from flask_principal import identity_changed, Identity, AnonymousIdentity
from ..config import BlogSettings
from .permissions import admin_Permission, su_Permission
from flask.views import MethodView


def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog_admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.objects.get(username=form.username.data)
        except User.DoesNotExist:
            user = None

        if user and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            user.last_login = datetime.datetime.now
            user.save()
            identity_changed.send(current_app._get_current_object(), identity=Identity(user.username))
            return redirect(request.args.get('next') or url_for('blog_admin.index'))

        flash('Invalid username or password', 'danger')

    return render_template('useraccounts/login.html', form=form)


def register(admin_create=False):
    if admin_create and not BlogSettings['allow_admin_creation']:
        msg = 'Administrator creation is forbidden,Please contact author'
        abort(403, msg)

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data

        if admin_create and BlogSettings['allow_admin_creation']:
            user.is_superuser = True
        user.save()

        return redirect(url_for('useraccounts.login'))

    return render_template('useraccounts/register.html', form=form)


@login_required
def logout():
    logout_user()
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    identity_changed.send(current_user._get_current_object(), identity=AnonymousIdentity())

    flash('You have been logged out', 'success')

    return redirect(url_for('useraccounts.login'))


class Users(MethodView):
    template_name = 'useraccounts/users.html'
    decorators = [login_required, su_Permission.require(401)]

    def get(self):
        users = User.objects.all()
        return render_template(self.template_name, users=users)




