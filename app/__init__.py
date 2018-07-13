import os
from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine
from flask_moment import Moment
from .config import config

db = MongoEngine()
moment = Moment()
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__, template_folder=config[config_name].TEMPLATE_PATH,
                static_folder=config[config_name].STATIC_PATH)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    from main.urls import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from useraccounts.urls import accounts as accounts_blueprint
    app.register_blueprint(accounts_blueprint)

    return app






