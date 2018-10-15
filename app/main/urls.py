from flask import Blueprint
from . import views, admin_view, errors


main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', views.list_post)
main.add_url_rule('/posts/', 'posts', views.list_post)
main.add_url_rule('/post/<post_id>/', 'post_detail', views.post_detail, methods=['GET', 'POST'])

main.errorhandler(401)(errors.handle_unauthorized)


blog_admin = Blueprint('blog_admin', __name__)
blog_admin.add_url_rule('/', view_func=admin_view.AdminIdx.as_view('index'))
blog_admin.add_url_rule('/send-confirm/', 'send_confirm', admin_view.send_confirmation)
blog_admin.add_url_rule('/email-confirm/<token>/', view_func=admin_view.ConfirmEmail.as_view('confirm_email'))

blog_admin.add_url_rule('/new-report/', view_func=admin_view.Post.as_view('new_report'))
blog_admin.add_url_rule('/posts/<post_id>/', view_func=admin_view.Post.as_view('edit_post'))
blog_admin.add_url_rule('/posts/', view_func=admin_view.PostLists.as_view('posts'))
blog_admin.add_url_rule('posts/draft/', view_func=admin_view.DraftLists.as_view('drafts'))

blog_admin.add_url_rule('/posts/comments', view_func=admin_view.Comment.as_view('comments'))
blog_admin.add_url_rule('posts/comments/approved/', view_func=admin_view.Comment.as_view('comments_approved'),
                        defaults={'disabled': 'True'})
blog_admin.add_url_rule('/posts/comments/<pickup>/action/', view_func=admin_view.Comment.as_view('action'))

blog_admin.errorhandler(401)(errors.handle_unauthorized)

