from flask_principal import Principal, Permission, RoleNeed, UserNeed, identity_loaded
from flask import current_app
from flask_login import current_user


# ROLES = (('admin', 'admin'),
#         ('editor', 'editor'),
#         ('reader', 'reader'))


# Create a permission with a single Need, in this case a RoleNeed.
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor')).union(admin_permission)
reader_permission = Permission(RoleNeed('reader')).union(editor_permission)
# 用法：
# # protect a view with a principal for that need
# @app.route('/admin')
# @admin_permission.require()
# def do_admin_index():
#     return Response('Only if you are an admin')

@identity_loaded.connect
# @identity_loaded.connect_via(current_app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'username'):
        identity.provides.add(UserNeed(current_user.username))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'role'):
        # for role in current_user.roles:
        identity.provides.add(RoleNeed(current_user.role))

    # Assuming the User model has a list of posts the user
    # has authored, add the needs to the identity
    # if hasattr(current_user, 'posts'):
    #     for post in current_user.posts:
    #         identity.provides.add(EditBlogPostNeed(unicode(post.id)))

    # reader_permission.allows(identity) 返回布尔类型 Whether the identity can access this permission.
    # identity.allows_read = reader_permission.allows(identity)
    identity.allows_read = identity.can(reader_permission)
    identity.allows_edit = editor_permission.allows(identity)
    identity.allowd_admin = admin_permission.allows(identity)



 # allows(identity)

 #    Whether the identity can access this permission.
 #    Parameters:	identity – The identity