#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db.models import Prefetch, CharField, functions, Value
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model

from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework import viewsets, mixins
from rest_framework.decorators import action

from modules.core.api.viewsets import ActionRouterMixin
from modules.core.api.pagination import DefaultPagination
from . import serializers

UserModel = get_user_model()


class ManageUserViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                        mixins.UpdateModelMixin, ActionRouterMixin,
                        viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = serializers.UserSerializer
    pagination_class = DefaultPagination

    def get_queryset(self):
        queryset = UserModel.objects\
            .prefetch_related(
                Prefetch('groups', queryset=Group.objects.all())
            )\
            .annotate(full_name=functions.Concat(
                'first_name', Value(' '), 'last_name', output=CharField(),
            ))

        search = self.request.GET.get('search', None)
        if search:
            queryset = queryset.filter(full_name__icontains=search)
        return queryset


class ManageGroupViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         ActionRouterMixin, mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, IsAdminUser)
    serializer_class = serializers.GroupSerializer

    def get_queryset(self):
        return Group.objects\
            .prefetch_related('user_set', 'permissions')\
            .defer('permissions__name', 'permissions__codename')\
            .order_by('name')

    @action(methods=['delete', 'put', 'patch'], detail=True)
    def users(self, request, pk):
        return self._action_router(
            request,
            {
                'delete': self._nested_delete('user_set'),
                'put': self._nested_put('user_set'),
                'patch': self._nested_patch('user_set'),
            }
        )
