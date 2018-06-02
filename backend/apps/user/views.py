#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from django.contrib import messages
from django.utils.timezone import now
from django.views.generic.base import RedirectView

from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError

from allauth.account import signals
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

from defender import utils
from defender.models import AccessAttempt

from . import serializers


class BlockedOriginList(APIView):
    permission_classes = (IsAuthenticated,)
    name = 'blocked-origin-list'

    def get(self, request):
        blocked = []
        username = self.request.user.email

        attempts = AccessAttempt.objects.filter(username=username)\
            .order_by('ip_address', '-attempt_time')\
            .distinct('ip_address').values('ip_address', 'attempt_time')

        for attempt in attempts:
            attempt['ttl'] = 0
            if utils.is_source_ip_already_locked(attempt['ip_address']):  # pragma: no branch
                ttl = utils.REDIS_SERVER.ttl(
                    utils.get_ip_blocked_cache_key(attempt['ip_address'])
                )
                if ttl is not None:  # pragma: no branch
                    attempt['ttl'] = ttl

                blocked.append(attempt)
        return Response(blocked, status=status.HTTP_200_OK)


class BlockedOriginDetail(APIView):
    permission_classes = (IsAuthenticated,)
    name = 'blocked-origin-detail'

    def delete(self, request, address):
        if not utils.is_valid_ip(address):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        username = self.request.user.email

        if not utils.is_source_ip_already_locked(address):
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        exists = AccessAttempt.objects.filter(
            username=username, ip_address=address
        ).exists()

        if not exists:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        utils.unblock_ip(address)

        return Response({}, status=status.HTTP_200_OK)


class AccessAttemptList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AccessAttemptSerializer
    name = 'access-list'

    def get_queryset(self):
        last_7days = now() - timedelta(days=7)
        return AccessAttempt.objects.filter(
            username=self.request.user.email,
            attempt_time__gt=last_7days
        ).order_by('-attempt_time')


class SessionList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SessionsSerializer
    name = 'session-list'

    def get_queryset(self):
        return self.request.user.session_set.filter(
            expire_date__gt=now()
        ).order_by('-updated_at')

    def get_queryset_context(self):
        return {'request': self.request}


class SessionDetail(generics.RetrieveDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SessionsSerializer
    name = 'session-detail'

    def get_queryset(self):
        return self.request.user.session_set

    def get_queryset_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.pk == self.request.session.session_key:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordChangesList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordChangesSerializer
    name = 'password-changes-list'

    def get_queryset(self):
        return self.request.user.password_changes.order_by('changed_at')


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
        except EmailAddress.DoesNotExist:  # pragma: no cover
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
        if pk is None:  # pragma: no cover
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
