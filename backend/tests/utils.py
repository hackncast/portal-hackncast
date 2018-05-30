#!/usr/bin/env python3
# encoding: utf-8

from collections import namedtuple
from contextlib import contextmanager
from functools import partial

from django.urls import reverse
from rest_framework.test import APIClient

from tests.factories import DEFAULT_PASSWORD

Response = namedtuple('Response', ['status_code', 'content'])


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
            return response.json()

    def get(self, url):
        response = self._client.get(url, format='json')
        return Response(response.status_code, self.__get_content(response))

    def post(self, url, data):
        response = self._client.post(url, data, format='json')
        return Response(response.status_code, self.__get_content(response))

    def put(self, url, data):
        response = self._client.put(url, data, format='json')
        return Response(response.status_code, self.__get_content(response))

    def patch(self, url, data):
        response = self._client.patch(url, data, format='json')
        return Response(response.status_code, self.__get_content(response))

    def delete(self, url):
        response = self._client.delete(url, format='json')
        return Response(response.status_code, self.__get_content(response))

    def options(self, url):
        response = self._client.options(url, format='json')
        return Response(response.status_code, self.__get_content(response))

    def head(self, url):
        response = self._client.head(url, format='json')
        return Response(response.status_code, self.__get_content(response))

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
