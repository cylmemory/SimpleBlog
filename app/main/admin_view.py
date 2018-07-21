from flask import request, redirect, render_template, url_for, abort, flash, g, current_app, send_from_directory
from flask.views import MethodView
from flask_login import login_required, current_user
from ..useraccounts.models import User


class adminIdx(MethodView):
    decorators = [login_required]

    def get(self):
        user = User.objects.get(username=current_user.get_id())
        return render_template('blog_admin/index.html', user=user)

