from flask import render_template


# 403 forbidden access
def handle_forbidden(e):
    return render_template('blog_admin/403.html', msg=e.description), 403

# 401 Authorization acess
def handle_unauthorized(e):
    return render_template('blog_admin/401.html'), 401
