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
from flask_login import LoginManager
from flask_principal import Principal
# from flaskext.markdown import markdown2   # 也不能高亮代码
# from flask_misaka import Misaka, misaka as m
# from pygments import highlight
# from pygments.formatters import HtmlFormatter
# from pygments.lexers import get_lexer_by_name

# 初始化扩展
bootstrap = Bootstrap()
db = MongoEngine()
principals = Principal()

# 初始化flask-login
login_manager = LoginManager()
login_manager.session_protection = 'strong' # 安全等级
login_manager.login_view = 'auth.login'     # 登录页面的端点


# class HighlighterRenderer(m.HtmlRenderer):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

#     def block_code(self, code, lang):
#         guess = 'python3'
#         if code.lstrip().startswith('<?php'):
#             guess = 'php'
#         elif code.lstrip().startswith(('<', '{%')):
#             guess = 'html+jinja'
#         elif code.lstrip().startswith(('function', 'var', '$')):
#             guess = 'javascript'

#         lexer = get_lexer_by_name(lang or guess, stripall=True)
#         return highlight(code, lexer, HtmlFormatter(linenos=True))


# misaka = Misaka(
#     # Misaka 使用自定义的 render
#     renderer=HighlighterRenderer(),
#     fenced_code=True,
#     underline=True,
#     highlight=True,
#     disable_indented_code=True,
#     space_headers=True,
#     strikethrough=True,
#     footnotes=True,
#     tables=True,
#     math=True)


def create_app(config_name):
    # 创建程序实例
    app = Flask(__name__)

    # 配置程序
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 初始化扩展
    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    principals.init_app(app)
    # Markdown(app)
    # misaka.init_app(app)


    # 注册main蓝本程序
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # 注册auth蓝本程序，并制定了url_prefix
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app