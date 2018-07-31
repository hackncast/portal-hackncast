#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission

from rest_framework import serializers


UserModel = get_user_model()


class UserGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('pk', 'name')
        read_only_fields = ('pk', 'name')


class UserSerializer(serializers.ModelSerializer):
    groups = UserGroupsSerializer(many=True, required=False)

    class Meta:
        model = UserModel
        fields = (
            'pk', 'username', 'first_name', 'last_name', 'email', 'is_active',
            'date_joined', 'last_login', 'groups', 'is_staff',
        )
        read_only_fields = (
            'pk', 'username', 'first_name', 'last_name', 'email',
            'date_joined', 'last_login', 'groups',
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
    all_permissions = tuple(Permission.objects
                            .prefetch_related('content_type')
                            .only('id', 'name', 'content_type__app_label'))

    def get_permissions(self, session):
        permissions = {}
        for permission in self.all_permissions:
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
