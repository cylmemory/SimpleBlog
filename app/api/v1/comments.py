from . import api
from ...main import models
from flask import jsonify, request


@api.route('/api/v1/comments/', methods=['GET'])
def get_comments():
    comments = models.Comment.objects.filter(disabled=False)
    data = [comment.comment_to_dict() for comment in comments]

    return jsonify(comments=data)


@api.route('/api/v1/comments/<comment_id>', methods=['GET'])
def get_comment(comment_id):
    comment = models.Comment.objects.get_or_404(id=comment_id)
    return jsonify(comment.comment_to_dict())


@api.route('/api/v1/posts/<post_id>/comments/', methods='GET')
def get_post_comments(post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        return jsonify({'error': 'post does not exist'}), 404
    comment = models.Comment.objects.get_or_404(post_id=post_id)
    return jsonify(comment.comment_to_dict())


@api.route('/api/v1/posts/<post_id>/new-comment/', methods=['POST'])
def create_post_comment(post_id):
    try:
        post = models.Post.objects.get(id=post_id)
    except models.Post.DoesNotExist:
        return jsonify({'error': 'post does not exist'}), 404

    data = request.get_json()
    comment = models.Comment()

    comment.post_id = data.get('post_id') or post.id
    comment.title = data.get('title') or post.title
    comment.author = data.get('author')
    comment.email = data.get('email')
    comment.body = data.get('body')
    comment.create_time = data.get('create_time')
    comment.disabled = data.get('disabled')
    comment.replay_to = data.get('replay_to')
    comment.gavatar_id = data.get('gavatar_id')
    comment.save()

    return jsonify(comment.comment_to_dict())
