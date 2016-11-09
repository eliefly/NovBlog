#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'eliefly'
__mtime__ = '11/8/16'
"""

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # MONGODB_SETTINGS = {'DB': 'NovBlogDev'}
    MONGO_DBNAME = 'NovBlogDev'



class TestingConfig(Config):
    TESTING = True
    # MONGODB_SETTINGS = {'DB': 'NovBlogTest'}
    MONGO_DBNAME = 'NovBlogTest'



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
