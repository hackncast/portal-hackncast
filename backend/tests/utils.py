#!/usr/bin/env python3
# encoding: utf-8

from collections import namedtuple
from contextlib import contextmanager
from functools import partial

from django.urls import reverse
from rest_framework.test import APIClient

from defender.connection import get_redis_connection

from tests.factories import DEFAULT_PASSWORD

REDIS_SERVER = get_redis_connection()
Response = namedtuple('Response', ['status_code', 'content', 'url'])


def part_reverse(name):
    def innert_part_reverse(name, *args, **kwargs):
        return reverse(name, args=args, **kwargs)

    return partial(innert_part_reverse, name)


class ApiClient:
    def __init__(self):
        self._client = APIClient()

    def __get_content(self, response):
        if response.status_code == 204:
            return None
        else:
            if response.content:
                return response.json()
            return None

    def get(self, url, *args, **kwargs):
        response = self._client.get(url, format='json', *args, **kwargs)
        if response.status_code == 302:
            return Response(response.status_code, None, response.get('location'))
        return Response(
            response.status_code, self.__get_content(response), None,
        )

    def post(self, url, data, *args, **kwargs):
        response = self._client.post(url, data, format='json', *args, **kwargs)
        return Response(
            response.status_code, self.__get_content(response), None,
        )

    def put(self, url, data, *args, **kwargs):
        response = self._client.put(url, data, format='json', *args, **kwargs)
        return Response(
            response.status_code, self.__get_content(response), None,
        )

    def patch(self, url, data, *args, **kwargs):
        response = self._client.patch(
            url, data, format='json', *args, **kwargs
        )
        return Response(
            response.status_code, self.__get_content(response), None,
        )

    def delete(self, url, *args, **kwargs):
        response = self._client.delete(url, format='json', *args, **kwargs)
        return Response(
            response.status_code, self.__get_content(response), None,
        )

    def options(self, url, *args, **kwargs):
        response = self._client.options(url, format='json', *args, **kwargs)
        return Response(
            response.status_code, self.__get_content(response), None,
        )

    def head(self, url, *args, **kwargs):
        response = self._client.head(url, format='json', *args, **kwargs)
        return Response(
            response.status_code, self.__get_content(response), None,
        )

    @contextmanager
    def auth(self, username=None, password=None, user=None,
             ignore_error=False):
        if user:
            success = self._client.login(username=user.username,
                                         password=DEFAULT_PASSWORD)
        elif username and password:
            success = self._client.login(username=username, password=password)
        else:
            raise Exception(
                'Please inform a username/password or a user object'
            )

        if not ignore_error and not success:
            raise Exception('Invalid user/password')

        yield self

        self._client.logout()
