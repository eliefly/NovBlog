#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'eliefly'
__mtime__ = '11/8/16'
"""


from flask import render_template, session, redirect, url_for, flash
from .. import db
from . import main
from .forms import NameForm


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
    return render_template('test.html', form=form, name=session.get('name'))
