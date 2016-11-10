#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'eliefly'
__mtime__ = '11/9/16'
"""

import unittest
from flask import current_app
from app import create_app, mongo


class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # PyMongo()对象删除数据库。删除方式通过dir一步步查对象属性找到...
        mongo.db.client.drop_database(mongo.db.name)
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

    def test_mongo_db(self):
        mongo.db.users.insert({'name':'eliefly', 'age': 27})
        self.assertTrue(mongo.db.users.find_one({'name': 'eliefly'})['age'] == 27)
