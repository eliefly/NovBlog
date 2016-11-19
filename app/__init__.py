#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'eliefly'
__mtime__ = '11/8/16'
"""

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mongoengine import MongoEngine 
from config import config

bootstrap = Bootstrap()
db = MongoEngine()


def create_app(config_name):
    # 创建程序实例
    app = Flask(__name__)
    # 配置程序
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化扩展
    bootstrap.init_app(app)
    db.init_app(app)

    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    return app