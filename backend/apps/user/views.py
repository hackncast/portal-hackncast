#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.views.generic.base import RedirectView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from allauth.account import signals
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

from . import serializers


class EmailList(APIView):
    permission_classes = (IsAuthenticated,)
    name = 'email-list'

    def get_serializer(self, *args, **kwargs):
        return serializers.EmailSerializer(*args, **kwargs)

    def get(self, request, pk=None):
        data = self.request.user.emailaddress_set.all().order_by('email')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def post(self, request, pk=None):
        serializer = self.get_serializer(
            data=request.data, context={'request': request},
        )
        if serializer.is_valid():
            email_address = serializer.save()
            get_adapter(self.request).add_message(
                self.request._request, messages.INFO,
                'account/messages/email_confirmation_sent.txt',
                {'email': serializer.validated_data['email']}
            )
            signals.email_added.send(
                sender=self.request._request.user.__class__,
                request=self.request._request, user=self.request._request.user,
                email_address=email_address
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResendEmailConfirmationView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            email = self.request.user.emailaddress_set.get(pk=pk)
        except EmailAddress.DoesNotExist:
            email = None
            return Response(status=status.HTTP_404_NOT_FOUND)

        get_adapter(request._request).add_message(
            request._request, messages.INFO,
            'account/messages/email_confirmation_sent.txt',
            {'email': email}
        )
        email.send_confirmation(request)
        return Response({}, status=status.HTTP_200_OK)


class RedirectPasswordReset(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, uidb64, token, *args, **kwargs):
        return '/admin/#/user/password/reset/token/{}/{}/'.format(
            uidb64, token
        )


class RedirectEmailConfirmation(RedirectView):
    permanent = False
    query_string = True

    def get_redirect_url(self, key, *args, **kwargs):
        return '/admin/#/user/email/confirmation/{}/'.format(key)
