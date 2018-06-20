#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

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

    class Meta:
        model = Group
        fields = ('pk', 'name', 'users')
        read_only_fields = ('pk', 'users')
