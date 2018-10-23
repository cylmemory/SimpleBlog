from flask import redirect, render_template, url_for, request, g, flash, session, abort, current_app
from flask.views import MethodView
from . import models, forms
from mongoengine.queryset.visitor import Q
from ..config import BlogSettings
from flask_login import current_user
from ..main import signals

PER_PAGE = BlogSettings['paginate'].get('per_page', 10)


def index():
    return render_template('main/index.html')


def list_post():
    posts = models.Post.objects.filter(status=0).order_by('-create_time')
    tags = posts.distinct('tags')

    cur_tag = request.args.get('tag')
    cur_category = request.args.get('category')
    cur_kws = request.args.get('keywords')

    if cur_tag:
        posts = posts.filter(tags=cur_tag)

    if cur_category:
        posts = posts.filter(category=cur_category)

    if cur_kws:
        posts = posts.filter(Q(content__icontains=cur_kws) | Q(title__icontains=cur_kws) | Q(abstract__icontains=cur_kws))

    # use mongoengine's _get_collection() function to query aggregate
    cursor_for_category = models.Post._get_collection().aggregate([
        {
            '$group': {'_id': {'category': '$category'}, 'name': {'$first': '$category'}, 'count': {'$sum': 1}}
        }
        ])

    try:
        cur_page = int(request.args.get('page', 1))
    except ValueError:
        cur_page = 1

    posts = posts.paginate(page=cur_page, per_page=PER_PAGE)

    data = { }

    data['posts'] = posts
    data['tags'] = tags
    data['cur_tag'] = cur_tag
    data['cur_category'] = cur_category
    data['keywords'] = cur_kws
    data['cursor_for_category'] = cursor_for_category

    return render_template('main/index.html', **data)


def post_detail(post_id, is_preview=False):
    post = models.Post.objects.get_or_404(id=post_id)

    if post.status == 1 and current_user.is_anonymous:
        abort(404)
    data = {}
    data['allow_share_article'] = BlogSettings['allow_share_article']
    data['allow_comment'] = BlogSettings['allow_comment']
    data['post'] = post

    if request.form:
        form = forms.CommentForm(obj=request.form)
    else:
        obj = {'email': session.get('email'), 'author': session.get('author'),}
        form = forms.CommentForm(**obj)
    if form.validate_on_submit():
        '''commit comment.'''
        comment = models.Comment()
        comment.author = form.author.data.strip()
        comment.email = form.email.data.strip()
        comment.post_id = post_id
        comment.post_title = post.title
        comment.body = form.body.data.strip()
        comment.save()

        session['email'] = form.email.data.strip()
        session['author'] = form.author.data.strip()

        url = '{0}#comment'.format(url_for('main.post_detail', post_id=post_id))
        url = '{0}#comment'.format(request.full_path)
        msg = 'Succeed to comment, and it will be displayed when the administrator reviews it.'
        flash(msg, 'success')
        return redirect(url)

    if data['allow_comment']:
        data['comment_html'] = post_comment(post_id, form) if post_comment else ''

    if not is_preview:
        signals.post_visited.send(current_app._get_current_object(), post=post)

    template_name = 'main/post.html'

    return render_template(template_name, **data)


def post_comment(post_id, form=None, *args, **kwargs):
    # view method of comment form.
    template_name = 'main/comments.html'
    comments = models.Comment.objects(post_id=post_id, disabled=False).order_by('create_time')

    data = {
        'form': form,
        'comments': comments if comments else '',
        'slug': post_id,
    }

    return render_template(template_name, **data)

def author_info(username):
    author = models.User.objects.get_or_404(username=username)

    posts = models.Post.objects.filter(status=0, author=author).order_by('-create_time')
    cur_page = request.args.get('page', 1)

    posts = posts.paginate(page=int(cur_page), per_page=10)

    data={}
    data['user'] = author
    data['posts']= posts

    return render_template('main/author.html', **data)
