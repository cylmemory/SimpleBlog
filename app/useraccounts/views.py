from flask import redirect, render_template, url_for, request, g, flash, session, current_app
from .. import db
from . import models
from . import forms
from flask_login import logout_user, current_user
import datetime
from flask_principal import identity_changed, Identity


def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.objects.get(username = form.Username.data)
        except models.User.DoesNotExist:
            user = None
        if user or user.verify_password(form.Password.data):
            logout_user(user, form.remember_me.data)
            user.last_login_time = datetime.datetime.now
            user.save()
            identity_changed.send(current_app._get_current_object(), identity=Identity(current_user.username))
            return redirect(request.args.get('next') or url_for('blog_admin.html'))
        flash('Invalid username or password', 'danger')
    render_template('useraccounts/login.html', form=form)
