from flask import render_template
from . import auth

@auth.app_errorhandler(404)
def page_not_found(e):
    return render_template('auth/404.html'), 404

@auth.app_errorhandler(401)
def page_unauthorized(e):
    return render_template('auth/401.html'), 401    # why?出现了401错误，但没有预期401.html
