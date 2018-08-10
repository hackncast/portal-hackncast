#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import viewsets as views
from modules.core.api.router import routerFactory

router = routerFactory(
    (r'access', views.AccessAttemptViewSet, "access"),
    (r'access/blocked', views.BlockedOriginViewSet, "blocked-origin"),
    (r'session', views.SessionViewSet, "session"),
    (r'password', views.PasswordChangesViewSet, "password-changes"),
    (r'email', views.EmailViewSet, "email"),
)

urlpatterns = router.urls
