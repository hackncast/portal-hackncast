#!/usr/bin/env python
# -*- coding: utf-8 -*-


def password_changed(sender, instance, *args, **kwargs):
    if instance:
        new_password = instance.password
        try:
            old_password = sender.objects.get(pk=instance.pk).password
        except sender.DoesNotExist:
            old_password = None
        if new_password != old_password:
            from apps.user.models import PasswordChanges
            PasswordChanges.objects.create(user=instance)
