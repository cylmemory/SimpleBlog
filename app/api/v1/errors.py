from . import api
from flask import jsonify


def bad_request_error(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400

    return response


def unauthorized_error(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401

    return response


def forbidden_error(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403

    return response


def page_not_found_error(message):
    response = jsonify({'error': 'page not found', 'message': message})
    response.status_code = 404

    return response


class ValidationError(ValueError):
    pass


@api.errorhandler(ValidationError)
def validate_error(e):
    return bad_request_error(e.args[0])
