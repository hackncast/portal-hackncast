#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from . import viewsets as views

urlpatterns = [
    path('access/',
         views.AccessAttemptList.as_view(), name=views.AccessAttemptList.name),
    path('access/blocked/',
         views.BlockedOriginList.as_view(), name=views.BlockedOriginList.name),
    path('access/blocked/<address>',
         views.BlockedOriginDetail.as_view(),
         name=views.BlockedOriginDetail.name),
    path('session/',
         views.SessionList.as_view(), name=views.SessionList.name),
    path('session/<pk>/',
         views.SessionDetail.as_view(), name=views.SessionDetail.name),
    path('password/',
         views.PasswordChangesList.as_view(),
         name=views.PasswordChangesList.name),
    path('email/', views.EmailList.as_view(), name=views.EmailList.name),
    path('email/<pk>/',
         views.EmailDetail.as_view(), name=views.EmailDetail.name),
    path('email/<pk>/send_confirmation/',
         views.ResendEmailConfirmationView.as_view(),
         name='resend_email_confirmation'),

    # Redirects
    path('reset/<uidb64>/<token>/',
         views.RedirectPasswordReset.as_view(), name='password_reset_confirm'),
    path('account-confirm-email/<key>/',
         views.RedirectEmailConfirmation.as_view(),
         name='account_confirm_email'),
]
