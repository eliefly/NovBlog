from flask import render_template, redirect, url_for, flash, request
from . import auth
from .forms import LoginForm
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user


@auth.route('/')
def index():
    return render_template('auth/index.html', current_user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get(username=form.username.data)
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            if current_user.is_authenticated:
                flash('%s login successfully.' % (current_user.username))
            next = request.args.get('next')
            return redirect(next or url_for('auth.index'))
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form, current_user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.index'))