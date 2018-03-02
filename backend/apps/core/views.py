#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_auth.registration.views import RegisterView
from rest_auth.views import PasswordResetView
from . import serializers


class CaptchaRegisterView(RegisterView):
    serializer_class = serializers.CaptchaRegisterSerializer


class CaptchaPasswordResetView(PasswordResetView):
    serializer_class = serializers.CaptchaPasswordResetSerializer
