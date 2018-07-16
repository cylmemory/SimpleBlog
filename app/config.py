import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'fjdljLJDL08_80jflKzcznv*c'
    MONGODB_SETTINGS = {'DB': 'Tools'}

    TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates').replace('\\', '/')
    STATIC_PATH = os.path.join(BASE_DIR, 'static').replace('\\', '/')
    EXPORT_PATH = os.path.join(BASE_DIR, 'exports').replace('\\', '/')

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
        'db': os.environ.get('DB_NAME') or 'OctBlog',
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
    'testing': TestingConfig
}
