#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import timedelta

from allauth.account import signals
from allauth.account.adapter import get_adapter
from allauth.account.models import EmailAddress

from defender import utils
from defender.models import AccessAttempt

from django.contrib import messages
from django.utils.timezone import now
from django.views.generic.base import RedirectView

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from modules.core.api.viewsets import ListOnlyViewSet

from . import serializers


class BlockedOriginViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'address'
    lookup_value_regex = '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'

    def list(self, request):
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

    def destroy(self, request, address=None):
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


class AccessAttemptViewSet(ListOnlyViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.AccessAttemptSerializer

    def get_queryset(self):
        last_7days = now() - timedelta(days=7)
        return AccessAttempt.objects.filter(
            username=self.request.user.email,
            attempt_time__gt=last_7days
        ).order_by('-attempt_time')


class SessionViewSet(mixins.DestroyModelMixin, viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.SessionsSerializer

    def get_queryset(self):
        queryset = self.request.user.session_set
        if self.action == 'list':
            queryset = queryset.filter(
                expire_date__gt=now()
            ).order_by('-updated_at')
        return queryset

    # def get_queryset_context(self):
    #     return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.pk == self.request.session.session_key:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordChangesViewSet(ListOnlyViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.PasswordChangesSerializer

    def get_queryset(self):
        return self.request.user.password_changes.order_by('changed_at')


class EmailViewSet(mixins.CreateModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.EmailSerializer

    def get_queryset(self):
        return self.request.user.emailaddress_set.all().order_by('email')

    def create(self, request):
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

    def destroy(self, request, pk=None):
        email_address = self.get_object()
        if email_address.primary:
            messages.error(
                request,
                'You cannot exclude your primary email address ({})'.format(
                    email_address.email
                )
            )
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        email = email_address.email
        self.perform_destroy(email_address)
        signals.email_removed.send(
            sender=request.user.__class__, request=request._request,
            user=request.user, email_address=email_address,
        )
        messages.success(
            request, 'Email \'{}\' excluded successfully'.format(email)
        )
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post', 'get'], detail=False)
    def primary(self, request):
        if request.method == 'GET':
            queryset = self.get_queryset().get(primary=True)
            serializer = self.serializer_class(queryset)
        else:
            try:
                email = self.get_queryset().get(
                    pk=self.request.data.get('pk', None)
                )
            except EmailAddress.DoesNotExist:
                raise NotFound('Email address not found!')

            if not email.verified:
                get_adapter(request).add_message(
                    request, messages.ERROR,
                    'account/messages/unverified_primary_email.txt'
                )
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

            email.set_as_primary()
            get_adapter(request).add_message(
                request._request, messages.SUCCESS,
                'account/messages/primary_email_set.txt'
            )

            # Sending the old primary address to the signal, adds a db query.
            try:
                from_email_address = self.get_queryset().filter(primary=True)
            except EmailAddress.DoesNotExist:  # pragma: no cover
                from_email_address = None

            signals.email_changed.send(
                sender=request.user.__class__, request=request._request,
                user=request.user, from_email_address=from_email_address,
                to_email_address=email
            )
            serializer = self.serializer_class(email)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True)
    def resend(self, request, pk=None):
        email = self.get_object()
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
