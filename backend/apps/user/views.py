#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib import messages
from django.views.generic.base import RedirectView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError

from allauth.account import signals
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

from . import serializers


class EmailList(APIView):
    permission_classes = (IsAuthenticated,)
    name = 'email-list'

    def get_serializer(self, *args, **kwargs):
        return serializers.EmailSerializer(*args, **kwargs)

    def get(self, request):
        data = self.request.user.emailaddress_set.all().order_by('email')
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
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


class EmailDetail(APIView):
    permission_classes = (IsAuthenticated,)
    name = 'email-detail'

    def get_serializer(self, *args, **kwargs):
        return serializers.EmailSerializer(*args, **kwargs)

    def get(self, request, pk):
        try:
            data = self.request.user.emailaddress_set.get(pk=pk)
        except EmailAddress.DoesNotExist:
            raise NotFound('Email address not found!')

        serializer = self.get_serializer(data)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            email = request.user.emailaddress_set.get(pk=pk)
        except EmailAddress.DoesNotExist:
            raise NotFound('Email address not found!')

        query = EmailAddress.objects.filter(user=request.user, verified=True)
        if not email.verified and query.exists():
            get_adapter(request).add_message(
                request, messages.ERROR,
                'account/messages/unverified_primary_email.txt'
            )
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        # Sending the old primary address to the signal
        # adds a db query.
        try:
            from_email_address = EmailAddress.objects.get(
                user=request.user, primary=True
            )
        except EmailAddress.DoesNotExist:
            from_email_address = None
        email.set_as_primary()

        get_adapter(request).add_message(
            request._request, messages.SUCCESS,
            'account/messages/primary_email_set.txt'
        )
        signals.email_changed.send(
            sender=request.user.__class__, request=request._request,
            user=request.user, from_email_address=from_email_address,
            to_email_address=email
        )
        return Response({'email': email.email}, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        if pk is None:
            raise ParseError('Please specify the email address')

        try:
            email_address = request.user.emailaddress_set.get(pk=pk)
        except EmailAddress.DoesNotExist:
            raise NotFound('Email address not found!')

        if email_address.primary:
            messages.error(
                request,
                'You cannot exclude your primary email address ({})'.format(
                    email_address.email
                )
            )
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        email = email_address.email
        email_address.delete()
        signals.email_removed.send(
            sender=request.user.__class__, request=request._request,
            user=request.user, email_address=email_address
        )
        messages.success(
            request, 'Email \'{}\' excluded successfully'.format(email)
        )
        return Response({}, status=status.HTTP_200_OK)


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
