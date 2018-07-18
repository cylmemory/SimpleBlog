from flask import Blueprint
from . import views

accounts = Blueprint('useraccounts', __name__)

accounts.add_url_rule('/login/', 'login', views.login, methods=['GET', 'POST'])
accounts.add_url_rule('register', 'register', views.register, methods=['GET', 'POST'])
