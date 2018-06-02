#!/usr/bin/env python3
# encoding: utf-8

import re

from unittest import mock
from django.urls import reverse

from tests.factories import DEFAULT_PASSWORD

USER = reverse('rest_user_details')
CHANGE_PASSWORD = reverse('rest_password_change')
RESET_PASSWORD = reverse('rest_password_reset')
CONFIRM_RESET = reverse('rest_password_reset_confirm')
QUERY_HIBP = 'apps.core.password_validation.query_hibp'


def test_unauthorized_password_change(api_client):
    response = api_client.get(CHANGE_PASSWORD)
    assert response.status_code == 403
    response = api_client.post(CHANGE_PASSWORD, {})
    assert response.status_code == 403


def test_password_change(api_client, fake_users):
    user = fake_users()

    with api_client.auth(user=user):
        data = {
            'old_password': DEFAULT_PASSWORD,
            'new_password1': 'complex_psswd',
            'new_password2': 'complex_psswd',
        }
        with mock.patch(QUERY_HIBP) as mocked:
            mocked.return_value = (False, None)
            response = api_client.post(CHANGE_PASSWORD, data)

        assert response.status_code == 200
        assert response.content['detail'] == 'New password has been saved.'

    with api_client.auth(username=user.username, password='complex_psswd'):
        response = api_client.get(USER)
        assert response.status_code == 200


def test_password_reset(api_client, fake_users, mailoutbox):
    user = fake_users()
    data = {'email': user.email, 'recaptcha': 'PASSED'}
    assert len(mailoutbox) == 0

    response = api_client.post(RESET_PASSWORD, data)
    assert response.status_code == 200
    assert response.content['detail'] == 'Password reset e-mail has been sent.'
    assert len(mailoutbox) == 1

    # Reset Password Email
    m = mailoutbox[0]
    assert list(m.to) == [user.email]
    match = re.search(
        '(http://localhost:8080/api/user/reset/.+/.+-.+/)', m.body
    )
    assert match

    # Reset Password Redirect
    url = match.groups()[0].split('8080')[-1]
    uid = url.split('/')[-3]
    token = url.split('/')[-2]
    response = api_client.get(url)
    assert response.status_code == 302
    assert response.content is None
    assert response.url == \
        '/admin/#/user/password/reset/token/{}/{}/'.format(uid, token)

    # Post New Password
    data = {
        'new_password1': 'complex_psswd',
        'new_password2': 'complex_psswd',
        'uid': uid, 'token': token,
    }
    with mock.patch(QUERY_HIBP) as mocked:
        mocked.return_value = (False, None)
        response = api_client.post(CONFIRM_RESET, data)
    assert response.status_code == 200
    assert response.content['detail'] \
        == 'Password has been reset with the new password.'

    with api_client.auth(username=user.username, password='complex_psswd'):
        response = api_client.get(USER)
        assert response.status_code == 200


def test_pwned_password_change(api_client, fake_users):
    user = fake_users()

    with api_client.auth(user=user):
        data = {
            'old_password': DEFAULT_PASSWORD,
            'new_password1': 'senha123',
            'new_password2': 'senha123',
        }
        with mock.patch(QUERY_HIBP) as mocked:
            mocked.return_value = (True, 2)
            response = api_client.post(CHANGE_PASSWORD, data)
        assert response.status_code == 400
        assert 'pwned' in response.content['new_password2'][0]


def test_pwned_password_reset(api_client, fake_users, mailoutbox):
    user = fake_users()
    data = {'email': user.email, 'recaptcha': 'PASSED'}
    assert len(mailoutbox) == 0

    response = api_client.post(RESET_PASSWORD, data)
    assert response.status_code == 200
    assert response.content['detail'] == 'Password reset e-mail has been sent.'
    assert len(mailoutbox) == 1

    # Reset Password Email
    m = mailoutbox[0]
    assert list(m.to) == [user.email]
    match = re.search(
        '(http://localhost:8080/api/user/reset/.+/.+-.+/)', m.body
    )
    assert match

    # Reset Password Redirect
    url = match.groups()[0].split('8080')[-1]
    uid = url.split('/')[-3]
    token = url.split('/')[-2]
    response = api_client.get(url)
    assert response.status_code == 302
    assert response.content is None
    assert response.url == \
        '/admin/#/user/password/reset/token/{}/{}/'.format(uid, token)

    # Post New Password
    data = {
        'new_password1': 'senha123',
        'new_password2': 'senha123',
        'uid': uid, 'token': token,
    }
    with mock.patch(QUERY_HIBP) as mocked:
        mocked.return_value = (True, 2)
        response = api_client.post(CONFIRM_RESET, data)
    assert response.status_code == 400
    assert 'pwned' in response.content['new_password2'][0]
