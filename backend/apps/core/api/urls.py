#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from . import viewsets as views
from rest_auth import views as auth_views
from rest_auth.registration.views import VerifyEmailView

urlpatterns = [
    path('', views.RootView.as_view(), name=views.RootView.name),
    # Customized Views
    path('auth/registration/',
         views.CaptchaRegisterView.as_view(), name='rest_register'),
    path('auth/password/reset/',
         views.CaptchaPasswordResetView.as_view(), name='rest_password_reset'),

    # Django Rest Auth Original Views
    path('auth/registration/verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('auth/password/reset/confirm/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),
    path('auth/login/',
         views.CustomLoginView.as_view(), name='rest_login'),
    path('auth/logout/',
         auth_views.LogoutView.as_view(), name='rest_logout'),
    path('auth/user/',
         views.CustomUserDetailsView.as_view(), name='rest_user_details'),
    path('auth/password/change/',
         auth_views.PasswordChangeView.as_view(), name='rest_password_change'),
]
