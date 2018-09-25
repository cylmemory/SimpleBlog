#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


BlogSettings = {
    'allow_admin_creation': os.environ.get('allow_admin_creation', 'true').lower() == 'true',
    'paginate':{
        'per_page':int(os.environ.get('per_page', 5)),
        'admin_per_page': int(os.environ.get('admin_per_page', 10)),
    }
}


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjdlj324fs5ssjflKzcznv*c'
    MONGODB_SETTINGS = {'DB': 'Tools'}

    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates').replace('\\', '/')
    STATIC_PATH = os.path.join(BASE_DIR, 'static').replace('\\', '/')
    EXPORT_PATH = os.path.join(BASE_DIR, 'exports').replace('\\', '/')

    # email server
    ##############
    # If using STARTTLS with MAIL_USE_TLS = True, then use MAIL_PORT = 587.
    # If using SSL/TLS directly with MAIL_USE_SSL = True, then use MAIL_PORT = 465.
    ##############
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 465))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'false').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    if not os.path.exists(EXPORT_PATH):
        os.makedirs(EXPORT_PATH)

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    MONGODB_SETTINGS = {
        'db': os.environ.get('DB_NAME') or 'Tools',
        'host': os.environ.get('MONGO_HOST') or 'localhost',
        }


class TestingConfig(Config):
    TESTING = True
    DEBUG = True

    MONGODB_SETTINGS = {
        'db': 'ToolsTest',
        'is_mock': True
    }


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
