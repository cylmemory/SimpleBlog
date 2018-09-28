from flask import redirect, render_template, url_for, request, g, flash, session, abort
from flask.views import MethodView
from . import models
from mongoengine.queryset.visitor import Q
from ..config import BlogSettings
from flask_login import current_user

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
        posts.filter(Q(title__icontains=cur_kws) | Q(content__icontains=cur_kws))

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


def post_detail(id):
    post = models.Post.objects.get_or_404(id=id)

    if post.status == 1 and current_user.is_anonymous:
        abort(404)
    data = {}
    data['allow_share_article'] = BlogSettings['allow_share_article']
    data['post'] = post

    template_name = 'main/post.html'

    return render_template(template_name, **data)