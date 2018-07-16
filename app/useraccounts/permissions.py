#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_principal import identity_changed, RoleNeed, UserNeed,Permission
from flask_login import current_user


su_need = RoleNeed('su')

su_Permission = Permission(su_need)
admin_Permission = Permission(RoleNeed('admin')).union(su_Permission)
editor_Permission = Permission(RoleNeed('editor')).union(admin_Permission)
writer_Permission = Permission(RoleNeed('writer')).union(editor_Permission)
reader_Permission = Permission(RoleNeed('reader')).union(writer_Permission)


@identity_changed.connect_via(current_user)
def on_identity_changed(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'username'):
        identity.provides.add(UserNeed(current_user.username))

    if hasattr(current_user, 'role'):
        identity.provides.add(RoleNeed(current_user.role))

    if hasattr(current_user, 'is_superuser') or current_user.is_superuser:
        identity.provides.add(su_need(current_user.is_superuser))

    identity.allow_su = Permission.allows(identity)
    identity.allow_amdin = Permission.allows(identity)
    identity.allow_edit = Permission.allows(identity)
    identity.allow_write = Permission.allows(identity)