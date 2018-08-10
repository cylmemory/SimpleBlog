from flask import request, redirect, render_template, url_for, abort, flash, g, current_app, send_from_directory
from flask.views import MethodView
from flask_login import login_required, current_user
from ..useraccounts.models import User


def get_current_user():
    user = User.objects.get(username=current_user.get_id())
    return user


class AdminIdx(MethodView):
    decorators = [login_required]
    template_name = 'blog_admin/index.html'

    def get(self):
        user = get_current_user()
        return render_template(self.template_name, user=user)

