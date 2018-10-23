from flask import render_template


# 404 page not find
def page_not_found(e):
    return render_template('main/404.html'), 404


# 404 can not match
def handle_unmatchable(*args, **kwargs):
    return render_template('main/404.html'), 404


# 400 bad request
def handle_bad_request(e):
    return 'bad request!', 400


# 403 forbidden access
def handle_forbidden(e):
    return render_template('blog_admin/403.html', msg=e.description), 403


# 401 Authorization access
def handle_unauthorized(e):
    return render_template('blog_admin/401.html'), 401


# admin page not find
def admin_page_not_found(e):
    return render_template('blog_admin/404.html'), 404


