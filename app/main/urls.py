from flask import Blueprint
from . import views, admin_view, errors


main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', views.index)


blog_admin = Blueprint('blog_admin', __name__)
blog_admin.add_url_rule('/', view_func=admin_view.AdminIdx.as_view('index'))
blog_admin.add_url_rule('/send-confirm/', 'send_confirm', admin_view.send_confirmation)
blog_admin.add_url_rule('/email-confirm/<token>/', view_func=admin_view.ConfirmEmail.as_view('confirm_email'))

blog_admin.add_url_rule('/new-report/', view_func=admin_view.Post.as_view('new_report'))
