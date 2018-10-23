from . import api
from ...main import models
from flask import request, jsonify, abort


@api.route('/api/v1/posts/', methods=['GET'])
def get_post_list():
    posts = models.Post.objects.filter(status=0).order_by('-create_time')

    tag = request.args.get('tag')
    category = request.args.get('category')

    if tag:
        posts = posts.filter(tags=tag)
    if category:
        posts = posts.filter(category=category)
    data = [post.post_to_dict() for post in posts]

    return jsonify(posts=data)


@api.route('/api/v1/new-post/', methods=['POST'])
def create_post():
    if not request.json or 'title' not in request.json:
        abort(400)

    data = request.get_json()
    post = models.Post()
    post.title = data.get('title')
    post.abstract = data.get('abstract')
    post.content = data.get('content')
    post.author = data.get('author')
    post.tags = data.get('tag')
    post.category = data.get('category')
    post.status = data.get('status')
    post.create_time = data.get('create_time')
    post.modify_time = data.get('modify_time')

    post.save()

    return jsonify(post.post_to_dict())


@api.route('/api/v1/posts/<post_id>/', methods=['GET'])
def get_post_detail(post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        return jsonify({'error': 'post does not exist'}), 404

    return jsonify(post.post_to_dict())


@api.route('/api/v1/posts/<post_id>/', methods=['PUT'])
def update_post(post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        return jsonify({'error': 'post does not exist'}), 404
    if not request.json:
        abort(400)

    data = request.get_json()

    if not data.get('title'):
        return 'post title is not existed in request data', 400

    if not data.get('abstract'):
        return 'post abstract is not existed in request data', 400

    if not data.get('content'):
        return 'post content is not existed in request data', 400

    if not data.get('author'):
        return 'post author is not existed in request data', 400

    if not data.get('tag'):
        return 'post tag is not existed in request data', 400

    if not data.get('category'):
        return 'post category is not existed  in request data', 400

    if not data.get('status'):
        return 'post status is not existed  in request data', 400

    post.title = data['title']
    post.abstract = data['abstract']
    post.content = data['content']
    post.author = data['author']
    post.tags = data['tag']
    post.category = data['category']
    post.status = data['status']
    post.save()

    return jsonify(post.post_to_dict())


@api.route('/api/v1/posts/<post_id>/', methods=['PATCH'])
def update_post_patch(post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        return jsonify({'error': 'post does not exist'}), 404
    if not request.json:
        abort(400)

    data = request.get_json()

    post.title = data['title'] or post.title
    post.abstract = data['abstract'] or post.abstract
    post.content = data['content'] or post.content
    post.author = data['author'] or post.author
    post.tags = data['tag'] or post.tags
    post.category = data['category'] or post.category
    post.status = data['status'] or post.status
    post.save()

    return jsonify(post.post_to_dict())


@api.route('/api/v1/posts/<post_id>/', methods=['DELETE'])
def delete_post(post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        return jsonify({'error': 'post does not exist'}), 404

    post.delete()

    return jsonify({'result': True})
