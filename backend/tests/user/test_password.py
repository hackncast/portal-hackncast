#!/usr/bin/env python3
# encoding: utf-8

from unittest import mock
from django.urls import reverse

REGISTRATION = reverse('rest_register')
CHANGE_PASSWORD = reverse('rest_password_change')
PASSWORD_CHANGES = reverse('password-changes-list')
QUERY_HIBP = 'apps.core.password_validation.query_hibp'


def __register_user(api_client):
    data = {
        'email': 'test@test.com',
        'password1': 'some_password',
        'password2': 'some_password',
        'recaptcha': 'PASSED',
    }
    with mock.patch(QUERY_HIBP) as mocked:
        mocked.return_value = (False, None)
        response = api_client.post(REGISTRATION, data)
    assert response.status_code == 201


def test_unauthorized_password_change_access(api_client):
    response = api_client.get(PASSWORD_CHANGES)
    assert response.status_code == 403


def test_empty_password_change(api_client):
    __register_user(api_client)
    with api_client.auth(username='test@test.com', password='some_password'):
        response = api_client.get(PASSWORD_CHANGES)
        assert response.status_code == 200
        assert len(response.content) == 0


def test_many_password_change(api_client):
    __register_user(api_client)
    with api_client.auth(username='test@test.com', password='some_password'):
        response = api_client.get(PASSWORD_CHANGES)
        assert response.status_code == 200
        assert len(response.content) == 0

        data = {
            'old_password': 'some_password',
            'new_password1': 'second_psswd',
            'new_password2': 'second_psswd',
        }
        with mock.patch(QUERY_HIBP) as mocked:
            mocked.return_value = (False, None)
            response = api_client.post(CHANGE_PASSWORD, data)
        assert response.status_code == 200

        response = api_client.get(PASSWORD_CHANGES)
        assert response.status_code == 200
        assert len(response.content) == 1

        data = {
            'old_password': 'second_psswd',
            'new_password1': 'third_psswd',
            'new_password2': 'third_psswd',
        }
        with mock.patch(QUERY_HIBP) as mocked:
            mocked.return_value = (False, None)
            response = api_client.post(CHANGE_PASSWORD, data)
        assert response.status_code == 200

        response = api_client.get(PASSWORD_CHANGES)
        assert response.status_code == 200
        assert len(response.content) == 2
