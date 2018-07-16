from flask import Blueprint
from . import views

accounts = Blueprint('useraccounts', __name__)

accounts.add_url_rule('/', 'index', accounts.index)
