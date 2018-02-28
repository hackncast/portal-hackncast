#!/usr/bin/env python
# -*- coding: utf-8 -*-

from recaptcha.fields import ReCaptchaField
from rest_auth.registration.serializers import RegisterSerializer


class CaptchaRegisterSerializer(RegisterSerializer):
    recaptcha = ReCaptchaField(write_only=True)
