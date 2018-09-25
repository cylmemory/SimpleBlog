from flask import request, redirect, render_template, url_for, abort, flash, g, current_app, send_from_directory
from flask.views import MethodView
from flask_login import login_required, current_user
from ..useraccounts.models import User
from ..useraccounts import email
import datetime
from ..useraccounts.permissions import writer_Permission, editor_Permission
from . import models, forms
from ..config import BlogSettings

PER_PAGE = BlogSettings['paginate'].get('admin_per_page', 10)

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

    def post(self, post_id=None, form=None, status=0):
        form = forms.PostForm(obj=request.form)
        if not form.validate():
            return self.get(post_id, form)

        try:
            post = models.Post.objects.get_or_404(id=post_id)

        except:
            post = models.Post()
            post.author = get_current_user()

        post.title = form.title.data.strip()
        post.content = form.content.data.strip()
        post.abstract = form.abstract.data.strip() if form.abstract.data.strip() else post.content[:140]
        post.category = form.category.data.strip() if form.category.data.strip() else None
        post.tags = [tag.strip() for tag in form.tags.data.split(',')] if form.tags.data else None

        if request.form.get('publish'):
            post.status = 0
            post.save()
            msg = 'Succeed to publish the post'
            redirect_url = url_for('blog_admin.posts')

        elif request.form.get('draft'):
            post.status = 1
            post.save()
            msg = 'Succeed to publish the draft'
            redirect_url = url_for('blog_admin.drafts')

        flash(msg, 'success')
        return redirect(redirect_url)

class PostLists(MethodView):
    decorators = [login_required]
    template_name = 'blog_admin/posts.html'
    status = 0

    def get(self):
        posts = models.Post.objects.filter(status=self.status).order_by('-modify_time')

        if not g.identity.can(editor_Permission):
            posts = posts.filter(author=get_current_user())


        try:
            cur_page = int(request.args.get('page',1))
        except:
            cur_page = 1

        posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

        return render_template(self.template_name, posts=posts, status=self.status)

class DraftLists(PostLists):
    status = 1

