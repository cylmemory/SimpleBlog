from flask import request, redirect, render_template, url_for, abort, flash, g, current_app, send_from_directory
from flask.views import MethodView
from flask_login import login_required, current_user
from ..useraccounts.models import User
from ..useraccounts import email
import datetime

def get_current_user():
    user = User.objects.get(username=current_user.get_id())
    return user


class AdminIdx(MethodView):
    decorators = [login_required]
    template_name = 'blog_admin/index.html'

    def get(self):
        user = get_current_user()
        return render_template(self.template_name, user=user)


@login_required
def send_confirmation():
    if current_user.email:
        token = current_user.generate_confirmation_token()
        email.send_confirm_email(current_user.email, current_user, token)
        current_user.confirm_send_time = datetime.datetime.now()
        current_user.save()
        flash('A confirmation email has been sent to you by email,  please check your email to confirm.', 'success')
    else:
        flash('Please set your email first!', 'danger')
    return render_template('blog_admin/index.html', user=current_user)
