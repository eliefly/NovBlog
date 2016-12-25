#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'eliefly'
__mtime__ = '11/8/16'
"""


from flask import render_template, session, redirect, url_for, flash, request, current_app
from .. import db
from . import main
from .forms import NameForm
from ..models import User, Post

@main.route('/test', methods=['GET', 'POST'])
def test():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('main.test'))
    return render_template('main/test.html', form=form, name=session.get('name'))


@main.route('/')
def index():
    '''分页导航显示文章'''
    page = request.args.get('page', 1, type=int)
    pagination = Post.objects.order_by('-publish_time').paginate(
                page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items

    # posts = Post.objects().order_by('-publish_time').all()
    return render_template('main/index.html', posts=posts, title='首页', pagination=pagination)


@main.route('/post')
def get_post():
    return render_template('main/post.html', title='首页')