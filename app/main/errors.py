from flask import render_template


def handle_forbidden(e):
    return render_template('blog_admin/403.html', msg=e.description), 403
