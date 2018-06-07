#!/usr/bin/env python3
# encoding: utf-8

from rest_framework import routers


def routerFactory(*routes):
    router = routers.SimpleRouter()
    for route in routes:
        router.register(route[0], route[1], base_name=route[2])
    return router
