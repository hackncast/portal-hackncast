#!/usr/bin/env python3
# encoding: utf-8

import re

from django.urls import reverse

from tests.factories import DEFAULT_PASSWORD

CHANGE_PASSWORD = reverse('rest_password_change')
RESET_PASSWORD = reverse('rest_password_reset')


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
            'new_password1': 'complex_new_password',
            'new_password2': 'complex_new_password',
        }
        response = api_client.post(CHANGE_PASSWORD, data)
        assert response.status_code == 200
        assert response.content['detail'] == 'New password has been saved.'

    with api_client.auth(username=user.username, password='complex_new_password'):
        response = api_client.options(CHANGE_PASSWORD)
        assert response.status_code == 200


def test_password_reset(api_client, fake_users, mailoutbox):
    user = fake_users()
    data = {'email': user.email, 'recaptcha': 'PASSED'}
    assert len(mailoutbox) == 0

    response = api_client.post(RESET_PASSWORD, data)
    assert response.status_code == 200
    assert response.content['detail'] == 'Password reset e-mail has been sent.'
    assert len(mailoutbox) == 1

    m = mailoutbox[0]
    assert list(m.to) == [user.email]
    match = re.search(
        '(http://localhost:8080/api/user/reset/[a-zA-Z1-9]+/.+-.+/)', m.body
    )
    assert match

    url = match.groups()[0].split('8080')[-1]
    response = api_client.get(url)
    # TODO: End this...
    assert response == ''
