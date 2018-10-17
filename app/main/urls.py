from flask import Blueprint
from . import views, admin_view, errors


main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', views.list_post)
main.add_url_rule('/posts/', 'posts', views.list_post)
main.add_url_rule('/post/<post_id>/', 'post_detail', views.post_detail, methods=['GET', 'POST'])
main.add_url_rule('/posts/<post_id>/preview/', 'post_preview', views.post_detail, defaults={'is_preview': True})
main.add_url_rule('/users/<username>/', 'author_info', views.author_info)

main.errorhandler(404)(errors.page_not_found)
main.errorhandler(401)(errors.handle_unauthorized)
main.add_url_rule('/<path:invalid_path>', 'handle_unmatchable', errors.handle_unmatchable)


blog_admin = Blueprint('blog_admin', __name__)
blog_admin.add_url_rule('/', view_func=admin_view.AdminIdx.as_view('index'))
blog_admin.add_url_rule('/send-confirm/', 'send_confirm', admin_view.send_confirmation)
blog_admin.add_url_rule('/email-confirm/<token>/', view_func=admin_view.ConfirmEmail.as_view('confirm_email'))

blog_admin.add_url_rule('/new-report/', view_func=admin_view.Post.as_view('new_report'))
blog_admin.add_url_rule('/posts/<post_id>/', view_func=admin_view.Post.as_view('edit_post'))
blog_admin.add_url_rule('/posts/', view_func=admin_view.PostLists.as_view('posts'))
blog_admin.add_url_rule('posts/draft/', view_func=admin_view.DraftLists.as_view('drafts'))

blog_admin.add_url_rule('/posts/statistics/', view_func=admin_view.PostStatisticList.as_view('post_statistics'))
blog_admin.add_url_rule('/posts/statistics/<post_id>/', view_func=admin_view.PostStatisticDetail.as_view('post_statistics_detail'))

blog_admin.add_url_rule('/posts/comments', view_func=admin_view.Comment.as_view('comments'))
blog_admin.add_url_rule('posts/comments/approved/', view_func=admin_view.Comment.as_view('comments_approved'),
                        defaults={'disabled': False})
blog_admin.add_url_rule('/posts/comments/<pickup>/action/', view_func=admin_view.Comment.as_view('action'))
blog_admin.add_url_rule('/posts/comments/action/', view_func=admin_view.Comments.as_view('comments_clear_action'))

blog_admin.errorhandler(404)(errors.admin_page_not_found)
blog_admin.errorhandler(401)(errors.handle_unauthorized)
blog_admin.errorhandler(403)(errors.handle_forbidden)