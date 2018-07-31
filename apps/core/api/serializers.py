#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers
from recaptcha.fields import ReCaptchaField
from rest_auth.serializers import PasswordResetSerializer
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer as UserSerializer

UserModel = get_user_model()


class CaptchaRegisterSerializer(RegisterSerializer):
    recaptcha = ReCaptchaField(write_only=True)


class CaptchaPasswordResetSerializer(PasswordResetSerializer):
    recaptcha = ReCaptchaField(write_only=True)


class UserDetailsSerializer(UserSerializer):
    email_pk = serializers.SerializerMethodField()
    verified_email = serializers.SerializerMethodField()

    def get_verified_email(self, user):
        email = self.context.get('primary_email')
        return email.verified

    def get_email_pk(self, user):
        email = self.context.get('primary_email')
        return email.pk

    class Meta:
        model = UserModel
        fields = (
            'pk', 'username', 'first_name', 'last_name', 'date_joined',
            'email', 'is_active', 'is_superuser', 'verified_email', 'email_pk',
            'last_login',
        )
        read_only_fields = (
            'pk', 'date_joined', 'email', 'is_active', 'is_superuser',
            'verified_email', 'email_pk', 'last_login',
        )
