#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path(
        'reset/<uidb64>/<token>/',
        views.RedirectPasswordReset.as_view(),
        name='password_reset_confirm'
    ),
]
