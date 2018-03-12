#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from allauth.account.models import EmailAddress
from rest_framework import serializers
from allauth.account.forms import AddEmailForm

UserModel = get_user_model()


class EmailSerializer(serializers.ModelSerializer):
    def validate_email(self, value):
        self.request = self.context.get('request')
        self.add_form = AddEmailForm(
            data=self.initial_data, user=self.request.user
        )
        if not self.add_form.is_valid():
            raise serializers.ValidationError(self.add_form.errors)
        return value

    class Meta:
        model = EmailAddress
        fields = ('pk', 'email', 'verified', 'primary')
        read_only_fields = ('pk', 'verified', 'primary')
