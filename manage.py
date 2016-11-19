#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'eliefly'
__mtime__ = '11/8/16'
"""

import os
from app import create_app, db
from flask_script import Manager, Shell, Server


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db)

manager.add_command("shell", Shell(make_context=make_shell_context))

manager.add_command("runserver", Server(host='0.0.0.0', port=5000, use_debugger=True))

@manager.command
def test():
    '''执行单元测试'''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
 