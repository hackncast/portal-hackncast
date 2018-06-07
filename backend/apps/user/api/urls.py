#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path
from rest_framework import routers

from . import viewsets as views
from apps.core.api.router import routerFactory

router = routerFactory(
    (r'access', views.AccessAttemptViewSet, "access"),
    (r'access/blocked', views.BlockedOriginViewSet, "blocked-origin"),
    (r'session', views.SessionViewSet, "session"),
    (r'password', views.PasswordChangesViewSet, "password-changes"),
    (r'email', views.EmailViewSet, "email"),
)

urlpatterns = [
    # Redirects
    path('reset/<uidb64>/<token>/',
         views.RedirectPasswordReset.as_view(), name='password_reset_confirm'),
    path('account-confirm-email/<key>/',
         views.RedirectEmailConfirmation.as_view(),
         name='account_confirm_email'),
]

urlpatterns += router.urls
