import unittest
from app.models import User
from flask import current_app
from app import create_app, db

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_password_setter(self):
        u = User()
        u.password = 'cat'
        self.assertTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User()
        u.password = 'cat'
        with self.assertRaises(AttributeError):
            u.password
    
    def test_password_verification(self):
        u = User()
        u.password = 'cat'
        self.assertTrue(u.verify_password('cat'))
        self.assertFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User()
        u.password = 'cat'
        u2 = User()
        u2.password = 'dog'
        self.assertTrue(u.password_hash != u2.password_hash)
