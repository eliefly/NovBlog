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
    categories = Post.objects.distinct('category')

    # posts = Post.objects().order_by('-publish_time').all()
    return render_template('main/index.html', posts=posts, title='首页', pagination=pagination, categories=categories)

@main.route('/example')
def post_example():
    return render_template('main/example.html', title='NovBlog')


@main.route('/post/<id>')
def get_post(id):
    post = Post.objects(id=id).first()
    return render_template('main/post.html', post=post, title='NovBlog文章')


@main.route('/posts/search/<text>', methods=['GET', 'POST'])
def post_search(text):
    page = request.args.get('page', 1, type=int)
    pagination = Post.objects.search_text(text).order_by('-publish_time').paginate(
                page, per_page=current_app.config['POSTS_PER_PAGE'], error_out=False)
    posts = pagination.items
    categories = Post.objects.distinct('category')

    return render_template('main/index.html', posts=posts, title=text + '-找找看', head='检索结果',
                pagination=pagination, categories=categories)