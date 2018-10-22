import unittest
from flask import current_app, url_for
from app import create_app, db


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db_name = current_app.config['MONGODB_SETTINGS']['db']
        db.connection.drop_database(db_name)
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get(url_for('main.index'))
        self.assertTrue(response.status_code == 200)

    def test_register_login_logout(self):
        response = self.client.post(url_for('useraccounts.register'), data={
            'username': 'test1',
            'email': 'test1@example.com',
            'password': 'test',
            'password2': 'test'
        })
        self.app.logger.debug(response.status_code)
        self.assertTrue(response.status_code == 302)

        response = self.client.post(url_for('useraccounts.login'), data={
            'username': 'test',
            'password': 'test'
        }, follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertFalse('Invalid username or password' in data)

        response = self.client.get(url_for('useraccounts.logout'),
                                   follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertTrue('You have been logged out' in data)








