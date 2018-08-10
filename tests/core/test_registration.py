#!/usr/bin/env python3
# encoding: utf-8

import re

from unittest import mock
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()
REGISTRATION = reverse('rest_register')
VERIFY_EMAIL = reverse('rest_verify_email')
USER = reverse('rest_user_details')


def test_successfully_registration_with_email(api_client, mailoutbox):
    assert User.objects.count() == 0
    assert len(mailoutbox) == 0

    data = {
        'email': 'test@test.com',
        'password1': 'some_password',
        'password2': 'some_password',
        'recaptcha': 'PASSED',
    }
    with mock.patch('modules.core.password_validation.query_hibp') as mocked:
        mocked.return_value = (False, None)
        response = api_client.post(REGISTRATION, data)
    assert response.status_code == 201
    assert 'key' in response.content
    assert len(mailoutbox) == 1

    m = mailoutbox[0]
    match = re.search(
        '(http://testserver/api/user/account-confirm-email/.+/)', m.body
    )
    assert list(m.to) == ['test@test.com']
    assert match

    verify_url = match.groups()[0].split('testserver')[-1]
    assert verify_url != ''
    key = verify_url.split('/')[-2]

    response = api_client.get(verify_url)
    assert response.status_code == 302
    assert response.content is None
    assert response.url == '/admin/#/user/email/confirmation/{}/'.format(key)

    with api_client.auth(username='test@test.com', password='some_password'):
        response = api_client.get(USER)
        assert response.status_code == 200
        assert response.content['username'] == 'test'
        assert response.content['email'] == 'test@test.com'
        assert response.content['is_active'] is True
        assert response.content['is_superuser'] is False
        assert response.content['verified_email'] is False

    data = {'key': key}
    response = api_client.post(VERIFY_EMAIL, data)
    assert response.status_code == 200

    with api_client.auth(username='test@test.com', password='some_password'):
        response = api_client.get(USER)
        assert response.status_code == 200
        assert response.content['verified_email'] is True


def test_pwned_password_registration(api_client, mailoutbox):
    assert User.objects.count() == 0
    assert len(mailoutbox) == 0

    data = {
        'email': 'test@test.com',
        'password1': 'password',
        'password2': 'password',
        'recaptcha': 'PASSED',
    }
    with mock.patch('modules.core.password_validation.query_hibp') as mocked:
        mocked.return_value = (True, 2)
        response = api_client.post(REGISTRATION, data)

    assert response.status_code == 400
    assert 'pwned' in response.content['password1'][0]
    assert len(mailoutbox) == 0
