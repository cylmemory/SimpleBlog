from . import api
from ...useraccounts import models
from flask import jsonify, abort, request


@api.route('/api/v1/users/', methods=['GET'])
def get_user_list():
    users = models.User.objects.all().order_by('-create_time')
    data = [user.user_to_dict() for user in users]

    return jsonify(users=data)


@api.route('/api/v1/new-user/', methods=['POST'])
def create_user():
    if not request.json or 'username' not in request.json:
        abort(400)

    data = request.get_json()

    user = models.User()
    user.username = data.get['username']
    user.email = data.get['email']
    user.confirmed = data.get['confirmed']
    user.role = data.get['role']
    user.is_superuser = data.get['is_superuser']
    user.about_me = data.get['about_me']
    user.social_networks = data.get['social_networks']
    user.last_login_time = data.get['last_login_time']
    user.create_time = data.get['create_time']
    user.username = data.get['confirm_send_time']
    user.save()

    return jsonify(user.user_to_dict())


@api.route('/api/v1/users/<user_id>/', methods=['GET'])
def get_user_detail(user_id):
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return jsonify({'error': 'user does not exist'}), 404

    return jsonify(user.user_to_dict())


@api.route('/api/v1/users/<user_id>/', methods=['PUT'])
def update_user(user_id):
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return jsonify({'error': 'user does not exist'}), 404
    if not request.json:
        abort(400)

    data = request.get_json()

    if not data.get['username']:
        return 'user username is not existed in request data', 400

    if not data.get['email']:
        return 'user email is not existed in request data', 400

    if not data.get['confirmed']:
        return 'user confirmed is not existed in request data', 400

    if not data.get['role']:
        return 'user role is not existed in request data', 400

    if not data.get['is_superuser']:
        return 'user is_superuser is not existed in request data', 400

    if not data.get['about_me']:
        return 'user about_me is not existed in request data', 400

    if not data.get['social_networks']:
        return 'user social_networks is not existed in request data', 400

    if not data.get['last_login_time']:
        return 'user last_login_time is not existed in request data', 400

    if not data.get['confirm_send_time']:
        return 'user confirm_send_time is not existed in request data', 400

    if not data.get['create_time']:
        return 'user create_time is not existed in request data', 400

    user.username = data['username']
    user.email = data['email']
    user.confirmed = data['confirmed']
    user.role = data['role']
    user.is_superuser = data['is_superuser']
    user.about_me = data['about_me']
    user.social_networks = data['social_networks']
    user.last_login_time = data['last_login_time']
    user.confirm_send_time = data['confirm_send_time']
    user.create_time = data['create_time']
    user.save()

    return jsonify(user.user_to_dict())


@api.route('/api/v1/users/<user_id>/', methods=['PATCH'])
def update_user_patch(user_id):
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return jsonify({'error': 'user does not exist'}), 404
    if not request.json:
        abort(400)

    data = request.get_json()

    user.username = data['username'] or user.username
    user.email = data['email'] or user.email
    user.confirmed = data['confirmed'] or user.confirmed
    user.role = data['role'] or user.role
    user.is_superuser = data['is_superuser'] or user.is_superuser
    user.about_me = data['about_me'] or user.about_me
    user.social_networks = data['social_networks'] or user.social_networks
    user.last_login_time = data['last_login_time'] or user.last_login_time
    user.confirm_send_time = data['confirm_send_time'] or user.confirm_send_time
    user.create_time = data['create_time'] or user.create_time
    user.save()

    return jsonify(user.user_to_dict())


@api.route('/api/v1/users/<user_id>/', methods=['DELETE'])
def update_user_patch(user_id):
    try:
        user = models.User.objects.get(id=user_id)
    except models.User.DoesNotExist:
        return jsonify({'error': 'user does not exist'}), 404

    user.delete()

    return jsonify({'result': True})

