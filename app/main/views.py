from flask import redirect, render_template, url_for, request, g, flash, session
from flask.views import MethodView

def index():
    return render_template('main/index.html')

def list_post():
    pass


