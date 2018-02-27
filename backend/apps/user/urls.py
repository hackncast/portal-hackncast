#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path(
        'email/<pk>/send_confirmation',
        views.ResendEmailConfirmationView.as_view(),
        name='resend_email_confirmation'
    ),

    # Redirects
    path(
        'reset/<uidb64>/<token>/',
        views.RedirectPasswordReset.as_view(),
        name='password_reset_confirm'
    ),
    path(
        'account-confirm-email/<key>/',
        views.RedirectEmailConfirmation.as_view(),
        name='account_confirm_email'
    ),
]
