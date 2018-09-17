from flask import request, redirect, render_template, url_for, abort, flash, g, current_app, send_from_directory
from flask.views import MethodView
from flask_login import login_required, current_user
from ..useraccounts.models import User
from ..useraccounts import email
import datetime
from ..useraccounts.permissions import writer_Permission, editor_Permission
from . import models, forms

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
    user = current_user
    if user.email:
        token = user.generate_confirmation_token()
        email.send_confirm_email(current_user.email, current_user, token)
        user.confirm_send_time = datetime.datetime.now()
        user.save()
        flash('A confirmation email has been sent to you by email,  please check your email to confirm.', 'success')
    else:
        flash('Please set your email first!', 'danger')

    return render_template('blog_admin/index.html', user=user)


class ConfirmEmail(MethodView):
    decorators = [login_required]

    def get(self, token):
        if current_user.confirmed:
            return redirect(url_for('blog_admin.index'))

        if current_user.confirm_email(token):
            flash('Your email has been confirmed', 'success')
        else:
            flash('The confirmation link is invalid or has expired', 'danger')

        return redirect(url_for('blog_admin.index'))

class Post(MethodView):
    decorators = [login_required, writer_Permission.require(401)]
    template_name = "blog_admin/post.html"

    def get(self, post_id=None, form=None, status=0):
        edit_flag = post_id is not None or False
        post = None

        if edit_flag:
            try:
                post = models.Post.objects.get(id=post_id)
            except models.Post.DoesNotExist:
                post = models.Post.objects.get_or_404(id=post_id)

            if not g.identity.can(editor_Permission) and Post.author.username != current_user.username:
                abort(401)

        if not form:
            if post:
                post.post_id = str(post.id)
                post.tags = ', '.join(post.tags)
                form = forms.PostForm(obj=post)
            else:
                form = forms.PostForm()

        categories = models.Post.objects(status=status).distinct('category')
        tags = models.Post.objects(status=status).distinct('tags')

        context = {'edit_flag': edit_flag, 'form': form, 'categories': categories, 'tags': tags}

        return render_template(self.template_name, **context)



