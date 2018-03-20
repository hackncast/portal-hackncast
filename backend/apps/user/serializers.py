#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from qsessions.models import Session
from rest_framework import serializers
from allauth.account.forms import AddEmailForm
from allauth.account.models import EmailAddress

from . import models

UserModel = get_user_model()


class EmailSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        self.request = self.context.get('request')
        self.add_form = AddEmailForm(
            data=self.initial_data, user=self.request._request.user
        )
        if not self.add_form.is_valid():
            raise serializers.ValidationError(self.add_form.errors)
        return value

    def save(self):
        self.add_form.save(self.request)

    class Meta:
        model = EmailAddress
        fields = ('pk', 'email', 'verified', 'primary')
        read_only_fields = ('pk', 'verified', 'primary')


class PasswordChangesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PasswordChanges
        fields = ('changed_at',)
        read_only_fields = ('changed_at',)


class SessionsSerializer(serializers.ModelSerializer):
    current = serializers.SerializerMethodField()

    def get_current(self, session):
        return session.pk == self.context.get('request').session.session_key

    class Meta:
        model = Session
        fields = ('pk', 'expire_date', 'user_agent', 'updated_at', 'ip',
                  'current')
        read_only_fields = ('pk', 'expire_date', 'user_agent', 'updated_at',
                            'ip', 'current')
