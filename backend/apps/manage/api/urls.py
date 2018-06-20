#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import viewsets as views
from apps.core.api.router import routerFactory

router = routerFactory(
    (r'user', views.ManageUserViewSet, "manage-user"),
    (r'group', views.ManageGroupViewSet, "manage-group"),
)

urlpatterns = router.urls
