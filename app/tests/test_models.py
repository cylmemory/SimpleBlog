import unittest
from flask import current_app, url_for
from app import create_app, db
from ..useraccounts import models as user_models
from ..main import models as main_models


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.context = self.app.context()
        self.app_context.push()

    def tearDown(self):
        db_name = current_app.config['MONGODB_SETTINGS']['DB']
        db.connection.drop_database(db_name)
        self.app_context.pop()

    def test_db_existing(self):
        self.assertTrue(current_app.config['MONGODB_SETTINGS'].get('DB') == 'ToolsTest')

    def test_create_user(self):
        user = user_models.User()

        user.username = 'test1'
        user.email = 'test1@gmail.com'
        user.password = '123'
        user.confirmed = False
        user.role = 'reader'
        user.about_me = 'This is a test user'
        user.save()

        created_user = user_models.User.objects.get(username='test1')

        self.assertTrue(created_user is not None and created_user.email == 'test1@gmail.com')

    def test_create_post(self):
        post = main_models.Post()

        post.title = 'test1'
        post.abstract = 'this is a test post'
        post.status = 0
        post.content = 'content'
        user = user_models.User()
        user.name = 'test1'
        user.password = '123'
        user.save()
        post.author = user
        post.tags = ['tag1']
        post.category = 'category1'

        post.save()

        created_post = main_models.Post.objects.get(title='test1').first()

        self.assertTrue(created_post is not None and created_post.content == 'content')






