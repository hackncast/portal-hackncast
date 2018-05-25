#!/usr/bin/env python3
# encoding: utf-8

from collections import namedtuple
from contextlib import contextmanager

from rest_framework.test import APIClient

from tests.factories import DEFAULT_PASSWORD

Response = namedtuple('Response', ['status_code', 'content'])


class ApiClient:
    def __init__(self):
        self._client = APIClient()

    def get(self, url):
        response = self._client.get(url, format='json')
        return Response(response.status_code, response.json())

    def post(self, url, data):
        response = self._client.post(url, data, format='json')
        return Response(response.status_code, response.json())

    def put(self, url, data):
        response = self._client.put(url, data, format='json')
        return Response(response.status_code, response.json())

    def patch(self, url, data):
        response = self._client.patch(url, data, format='json')
        return Response(response.status_code, response.json())

    def delete(self, url):
        response = self._client.delete(url, format='json')
        return Response(response.status_code, response.json())

    def options(self, url):
        response = self._client.options(url, format='json')
        return Response(response.status_code, response.json())

    def head(self, url):
        response = self._client.head(url, format='json')
        return Response(response.status_code, response.json())

    @contextmanager
    def auth(self, username=None, password=None, user=None):
        if user:
            success = self._client.login(username=user.username,
                                         password=DEFAULT_PASSWORD)
        elif username and password:
            success = self._client.login(username=username, password=password)
        else:
            raise Exception(
                'Please inform a username/password or a user object'
            )

        if not success:
            raise Exception('Invalid user/password')

        yield self
        self._client.logout()
