from flask import redirect, render_template, url_for, request, g, flash, session

def index():
    return render_template('main/index.html')

def list_post():
    pass
