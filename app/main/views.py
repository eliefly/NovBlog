#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'eliefly'
__mtime__ = '11/8/16'
"""


from flask import render_template
from .. import mongo
from . import main


@main.route('/')
def index():
    '''
    先在flask-script启动的shell中插入数据
    $ python manage.py shell
    >>> db
    Database(MongoClient(host=['localhost:27017'], document_class=dict, tz_aware=True, connect=True, replicaset=None), 'NovBlogDev')
    >>> user = {'name': 'eliefly', 'age':27, 'address':'shenzhen'}
    >>> db.users.insert_one(user)
    '''
    name = mongo.db.users.find_one()['name']
    return render_template('index.html', name=name)