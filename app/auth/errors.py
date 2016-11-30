from flask import render_template
from . import auth

@auth.app_errorhandler(401)
def page_unauthorized(e):
    return render_template('401.html'), 401    # why?出现了401错误，但没有预期401.html
