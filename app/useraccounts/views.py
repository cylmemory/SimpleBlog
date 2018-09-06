#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import redirect, render_template, url_for, request, g, flash, session, current_app, abort
from . import models
from .forms import LoginForm, RegistrationForm, UserForm, AddUserForm, UpdateProfileForm, ModifyPasswordForm, \
    ResetPasswordRequestForm, ResetPasswordForm
from flask_login import login_user, logout_user, current_user, login_required
import datetime
from flask_principal import identity_changed, Identity, AnonymousIdentity
from ..config import BlogSettings
from .permissions import admin_Permission, su_Permission
from flask.views import MethodView
from . import email

def login():
    if current_user.is_authenticated:
        return redirect(url_for('blog_admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.objects.get(username=form.username.data)
        except models.User.DoesNotExist:
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
        user = models.User()
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data

        if admin_create and BlogSettings['allow_admin_creation']:
            user.is_superuser = True
        user.save()
        flash('Register successful! Please login.', 'success')
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
        users = models.User.objects.all()
        return render_template(self.template_name, users=users)

class User(MethodView):
    template_name = 'useraccounts/user.html'
    decorators = [login_required, admin_Permission.require(401)]

    def get_context_data(self, username, form):
        if not form:
            user = models.User.objects.get_or_404(username=username)
            form = UserForm(obj=user)
        data = {'form': form, 'user': user}

        return data

    def get(self, username, form=None):
        data = self.get_context_data(username, form)
        return render_template(self.template_name, **data)

    def post(self, username):
        form = UserForm(request.form)
        if form.validate():
            user = models.User.objects.get(username=username)
            if user.email != form.email.data:
                user.confirmed = False
            user.email = form.email.data
            user.role = form.role.data
            user.is_superuser = (request.form.get('is_superuser') != None)
            user.confirmed = (request.form.get('confirmed') != None)
            user.save()
            flash('Update user detail successful', 'success')
            return redirect(url_for('useraccounts.edit-user', username=username))
        return self.get(username, form)

    def delete(self, username):
        user = models.User.objects.get_or_404(username=username)
        user.delete()
        if request.args.get('delete_tag'):
            return 'success'

        msg = 'Delete successful'
        flash(msg, 'success')
        return redirect(url_for('useraccounts.users'))


@login_required
def add_user():
    form = AddUserForm()
    if form.validate_on_submit():
        user = models.User()
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        user.role = form.role.data
        user.confirmed = (request.form.get('confirm') != None)
        user.save()
        flash('Success to add a new user !', 'success')
        return redirect(url_for('useraccounts.users'))
    return render_template('useraccounts/add_user.html', form=form)


class Profile(MethodView):
    template_name = 'useraccounts/setting.html'
    decorators = [login_required]

    def get_context_data(self, form):
        if not form:
            user = current_user
            user.github = user.social_networks['github'].get('url')
            user.wechat = user.social_networks['wechat'].get('url')
            user.weibo = user.social_networks['weibo'].get('url')
            user.twitter = user.social_networks['twitter'].get('url')
            user.facebook = user.social_networks['facebook'].get('url')
            form = UpdateProfileForm(obj=user)
        data = {'form': form}

        return data

    def get(self, form=None):
        data = self.get_context_data(form)
        return render_template(self.template_name, **data)

    def post(self):
        form = UpdateProfileForm(obj=request.form)
        if form.validate():
            user = current_user
            if user.email != form.email.data:
                user.email = form.email.data
                user.confirmed = False

            user.about_me = form.about_me.data
            user.homepage_url = form.homepage_url.data or None
            user.social_networks['github']['url'] = form.github.data or None
            user.social_networks['wechat']['url'] = form.wechat.data or None
            user.social_networks['weibo']['url'] = form.weibo.data or None
            user.social_networks['twitter']['url'] = form.twitter.data or None
            user.social_networks['facebook']['url'] = form.facebook.data or None
            user.save()

            flash('Success to update ！', 'success')
            return redirect(url_for('blog_admin.index'))
        return self.get(form)

@login_required
def update_password():
    form = ModifyPasswordForm()
    if form.validate_on_submit():
        user = current_user
        if form.current_password.data != form.confirm_password.data:
            user.password = form.confirm_password.data
            user.save()
            flash('success to update !', 'success')
            return redirect(url_for('useraccounts.password'))
        flash('New password is as same as current password.Please enter again!', 'danger')
    return render_template('useraccounts/update_password.html', form=form)


class Password(MethodView):
    template_name = 'useraccounts/update_password.html'
    decorators = [login_required]

    def get(self, form=None):
        if not form:
            form = ModifyPasswordForm()
        user = current_user
        data = {'form': form, 'user': user}

        return render_template(self.template_name, **data)

    def post(self):
        form = None

        if request.form.get('update'):

            form = ModifyPasswordForm(obj=request.form)
            if form.validate():
                user = current_user
                if form.current_password.data != form.confirm_password.data:
                    user.password = form.confirm_password.data
                    user.save()
                    flash('success to update!', 'success')
                    return  redirect(url_for('useraccounts.password'))

                flash('New password is as same as current password.Please enter again!', 'danger')
        return self.get(form)


class ResetPasswordRequest(MethodView):
    template_name = 'useraccounts/reset_password.html'

    def get(self, form=None):
        if not current_user.is_anonymous:
            return redirect(url_for('blog_admin.index'))
        if not form:
            form = ResetPasswordRequestForm()
        data = {'form': form}
        return render_template(self.template_name, **data)

    def post(self):
        form = ResetPasswordRequestForm(obj=request.form)

        if form.validate():
            user = models.User.objects(email=form.email.data.strip()).first()
            if user:
                token = user.generate_reset_token()
                email.send_reset_password_mail(user.email, user, token)
                flash('An email with instructions to reset your password has been sent to you')
                return redirect(url_for('useraccounts.login'))

            flash('User does not exist!', 'danger')
            return redirect(url_for('useraccounts.register'))

        return self.get(form)


class ResetPassword(MethodView):
    template_name = 'useraccounts/reset_password.html'

    def get(self, token, form=None):
        if not current_user.is_anonymous:
            return redirect(url_for('blog_admin.index'))

        if not form:
            form = ResetPasswordForm()
        data = {'form': form}

        return render_template(self.template_name, **data)

    def post(self, token):
        form = ResetPasswordForm(obj=request.form)

        if form.validate():
            flag = models.User.reset_password(token, form.new_password.data)

            if flag:
                flash('Your password has been updated.')
            else:
                flash('Fail to update your password')

            return redirect(url_for('useraccounts.login'))

        return self.get(form)



