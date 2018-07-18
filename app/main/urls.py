from flask import Blueprint
from . import views, errors


main = Blueprint('main', __name__)

main.add_url_rule('/', 'index', views.index)





