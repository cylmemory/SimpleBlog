from flask import Blueprint
from . import views
from ..main import errors

accounts = Blueprint('useraccounts', __name__)

accounts.add_url_rule('/login/', 'login', views.login, methods=['GET', 'POST'])
accounts.add_url_rule('/register/', 'register', views.register, methods=['GET', 'POST'])
accounts.add_url_rule('register/admin', 'register_admin', views.register, defaults={'admin_create': True},
                      methods=['GET', 'POST'])
accounts.add_url_rule('/logout/', 'logout', views.logout)
accounts.add_url_rule('/users/', view_func=views.Users.as_view('users'))
accounts.add_url_rule('/users/edit/<username>', view_func=views.User.as_view('edit-user'))
accounts.add_url_rule('/users/add_user', 'add_user', views.add_user, methods=['GET', 'POST'])
accounts.add_url_rule('user/setting', view_func=views.Profile.as_view('setting'))

accounts.errorhandler(403)(errors.handle_forbidden)
