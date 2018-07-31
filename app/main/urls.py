from flask import Blueprint
from . import views, admin_view, errors


main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', views.index)


blog_admin = Blueprint('blog_admin', __name__)
blog_admin.add_url_rule('/', view_func=admin_view.AdminIdx.as_view('index'))
