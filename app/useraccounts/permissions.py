#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_principal import identity_loaded, RoleNeed, UserNeed, Permission
from flask_login import current_user

su_need = RoleNeed('su')
admin_need = RoleNeed('admin')
editor_need = RoleNeed('editor')
writer_need = RoleNeed('writer')
reader_need = RoleNeed('reader')

su_Permission = Permission(su_need)
admin_Permission = Permission(admin_need).union(su_Permission)
editor_Permission = Permission(editor_need).union(admin_Permission)
writer_Permission = Permission(writer_need).union(editor_Permission)
reader_Permission = Permission(reader_need).union(writer_Permission)


@identity_loaded.connect
def on_identity_change(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'username'):
        identity.provides.add(UserNeed(current_user.username))

    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))

    if hasattr(current_user, 'is_superuser') and current_user.is_superuser:
        identity.provides.add(su_need)

    identity.allow_su = su_Permission.allows(identity)
    identity.allow_edit = editor_Permission.allows(identity)
    identity.allow_admin = admin_Permission.allows(identity)
    identity.allow_write = writer_Permission.allows(identity)
