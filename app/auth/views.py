from flask import render_template, redirect, url_for, flash, request, current_app, session, abort, g
from . import auth
from .forms import LoginForm, RegistrationForm
from ..models import User
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import Principal, Identity, AnonymousIdentity, identity_changed
from .permissions import admin_permission, editor_permission, reader_permission


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

            # Tell Flask-Principal the identity changed
            identity_changed.send(current_app._get_current_object(),
                                    identity=Identity(user.username))

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

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    flash('You have been logged out.')
    return redirect(url_for('auth.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data)
        user.password = form.password.data
        user.role = form.role.data
        user.save()
        flash('注册成功，现在可以登录了!')
    return render_template('auth/register.html', form=form)


@auth.route('/admin')
@login_required
# @reader_permission.require()    # user.role='reader',顺利访问
@admin_permission.require(http_exception=401)    # user.role='reader', flask_principal.PermissionDenied
def admin():
    # if not g.identity.can(admin_permission):
    #     abort(401)
    return render_template('auth/test_admin.html')