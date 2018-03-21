#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_auth.registration.views import RegisterView
from rest_auth.views import PasswordResetView, UserDetailsView

from . import serializers


class CaptchaRegisterView(RegisterView):
    serializer_class = serializers.CaptchaRegisterSerializer


class CaptchaPasswordResetView(PasswordResetView):
    serializer_class = serializers.CaptchaPasswordResetSerializer


class CustomUserDetailsView(UserDetailsView):
    serializer_class = serializers.UserDetailsSerializer

    def get_object(self):
        self.user = self.request.user
        self.primary_email = self.user.emailaddress_set.get(primary=True)
        return self.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['primary_email'] = self.primary_email
        return context
