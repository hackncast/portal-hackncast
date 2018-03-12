#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.urls import path

from . import views

urlpatterns = [
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
