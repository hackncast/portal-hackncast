#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from rest_framework import serializers


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    __all_groups = None

    @classmethod
    def all_groups(kls):
        if kls.__all_groups:
            return kls.__all_groups
        kls.__all_groups = tuple(
            Group.objects.order_by('name').only('id', 'name')
        )
        return kls.__all_groups

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        groups = []
        for _group in self.all_groups():
            group = {'pk': _group.pk, 'name': _group.name}
            group['participates'] = _group.pk in ret['groups']
            groups.append(group)

        ret['groups'] = groups
        return ret

    class Meta:
        model = UserModel
        fields = (
            'pk', 'username', 'first_name', 'last_name', 'email', 'is_active',
            'date_joined', 'last_login', 'groups', 'is_staff',
        )
        read_only_fields = (
            'pk', 'username', 'first_name', 'last_name', 'email',
            'date_joined', 'last_login',
        )


class GroupUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'pk', 'username', 'first_name', 'last_name', 'email', 'is_active',
            'is_staff',
        )
        read_only_fields = (
            'pk', 'username', 'first_name', 'last_name', 'email', 'is_active',
            'is_staff',
        )


class GroupSerializer(serializers.ModelSerializer):
    users = GroupUsersSerializer(source='user_set', many=True, read_only=True)
    permissions = serializers.SerializerMethodField()
    __all_permissions = None

    @classmethod
    def all_permissions(kls):
        if kls.__all_permissions:
            return kls.__all_permissions

        kls.__all_permissions = tuple(
            Permission.objects
            .prefetch_related('content_type')
            .only('id', 'name', 'content_type__app_label')
        )
        return kls.__all_permissions

    def get_permissions(self, session):
        permissions = {}
        for permission in self.all_permissions():
            label = permission.content_type.app_label
            ps = permissions.get(label, [])
            ps.append({
                'pk': permission.pk,
                'name': permission.name,
                'enabled': False,
            })
            permissions[label] = ps

        return permissions

    class Meta:
        model = Group
        fields = ('pk', 'name', 'users', 'permissions')
        read_only_fields = ('pk', 'users', 'permissions')
