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
    AVATER_FORMAT = list(['jpg', 'png', 'jpeg', 'bmp'])
    STATIC_FOLDER = '/home/eliefly/PycharmProjects/NovBlog/app/static'
    POSTS_PER_PAGE = 20

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    MONGODB_SETTINGS = {'db': 'NovBlogDev',
                        'ALIAS':'default',
                        'host': 'localhost'}


class TestingConfig(Config):
    TESTING = True
    MONGODB_SETTINGS = {'DB': 'NovBlogTest'}



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
