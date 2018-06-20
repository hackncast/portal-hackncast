#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import viewsets, mixins
from rest_auth.registration.views import RegisterView
from rest_auth.views import PasswordResetView, UserDetailsView, LoginView

from . import serializers
from .. import decorators, utils

watch_login = decorators.watch_login()


class RootView(APIView):
    name = 'root'

    def get(self, request):
        return Response(utils.getUrls(), status=status.HTTP_200_OK)


class CaptchaRegisterView(RegisterView):
    serializer_class = serializers.CaptchaRegisterSerializer


class CaptchaPasswordResetView(PasswordResetView):
    serializer_class = serializers.CaptchaPasswordResetSerializer


class CustomUserDetailsView(UserDetailsView):
    serializer_class = serializers.UserDetailsSerializer

    def get_object(self):
        self.user = self.request.user
        self.primary_email = self.user.emailaddress_set.get(primary=True)
        return self.user

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['primary_email'] = self.primary_email
        return context


class CustomLoginView(LoginView):
    @method_decorator(watch_login)
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ListOnlyViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class ActionRouterMixin:
    def __retrieve_pks(self, request):
        pks = request.data
        if isinstance(pks, str) or isinstance(pks, int):
            pks = [request.data]
        return pks

    def _nested_put(self, relation):
        def inner(instance, pks):
            getattr(instance, relation).set(pks)
            instance.save()
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return inner

    def _nested_patch(self, relation):
        def inner(instance, pks):
            if not pks:
                return Response(status=status.HTTP_204_NO_CONTENT)

            for pk in pks:
                getattr(instance, relation).add(pk)
            instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return inner

    def _nested_delete(self, relation):
        def inner(instance, pks):
            for pk in pks:
                getattr(instance, relation).remove(pk)
            instance.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return inner

    def _action_router(self, request, actionMap=None):
        method = self.request.method.lower()
        if method not in actionMap:  # pragma: no cover
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

        pks = self.__retrieve_pks(request)
        instance = self.get_object()
        return actionMap[method](instance, pks)
