#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_auth.registration.views import RegisterView

from . import serializers


class CaptchaRegisterView(RegisterView):
    serializer_class = serializers.CaptchaRegisterSerializer
