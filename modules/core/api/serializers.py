#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model

from rest_framework import serializers
from recaptcha.fields import ReCaptchaField
from rest_auth.serializers import PasswordResetSerializer
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import UserDetailsSerializer as UserSerializer
from allauth.account.models import EmailAddress

UserModel = get_user_model()


class CaptchaRegisterSerializer(RegisterSerializer):
    recaptcha = ReCaptchaField(write_only=True)


class CaptchaPasswordResetSerializer(PasswordResetSerializer):
    recaptcha = ReCaptchaField(write_only=True)


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailAddress
        fields = (
            'pk', 'email', 'verified', 'primary',
        )
        read_only_fields = (
            'pk', 'email', 'verified', 'primary',
        )


class UserDetailsSerializer(UserSerializer):
    emails = UserEmailSerializer(many=True, source="emailaddress_set")

    class Meta:
        model = UserModel
        fields = (
            'pk', 'username', 'first_name', 'last_name', 'date_joined',
            'emails', 'is_active', 'is_superuser', 'last_login'
        )
        read_only_fields = (
            'pk', 'date_joined', 'emails', 'is_active', 'is_superuser',
            'last_login'
        )
