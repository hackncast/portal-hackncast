#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from . import views
from rest_auth import views as auth_views
from rest_auth.registration.views import VerifyEmailView

app_name = 'core'
urlpatterns = [
    # Customized Views
    path('auth/registration/',
         views.CaptchaRegisterView.as_view(), name='rest_register'),

    # Django Rest Auth Original Views
    path('auth/registration/verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('auth/password/reset/',
         auth_views.PasswordResetView.as_view(), name='rest_password_reset'),
    path('auth/password/reset/confirm/',
         auth_views.PasswordResetConfirmView.as_view(),
         name='rest_password_reset_confirm'),
    path('auth/login/',
         auth_views.LoginView.as_view(), name='rest_login'),
    path('auth/logout/',
         auth_views.LogoutView.as_view(), name='rest_logout'),
    path('auth/user/',
         auth_views.UserDetailsView.as_view(), name='rest_user_details'),
    path('auth/password/change/',
         auth_views.PasswordChangeView.as_view(), name='rest_password_change'),
]
