#!/usr/bin/env python3
# encoding: utf-8

from django.urls import reverse

from defender import utils as defender
from django.test.client import RequestFactory

from tests.utils import part_reverse


LOGIN = reverse('rest_login')
ACCESS_ATTEMPTS = reverse('access-list')
BLOCKED_ORIGINS = reverse('blocked-origin-list')
BLOCKED_ORIGIN = part_reverse('blocked-origin-detail')
REDIS_SERVER = defender.REDIS_SERVER


def test_unauthorized_blocked_origin_access(api_client):
    response = api_client.get(BLOCKED_ORIGINS)
    assert response.status_code == 403

    response = api_client.get(BLOCKED_ORIGIN('127.0.0.1'))
    assert response.status_code == 403

    response = api_client.get(ACCESS_ATTEMPTS)
    assert response.status_code == 403


def test_empty_blocked_origin_list(api_client, fake_users):
    user = fake_users()
    with api_client.auth(user=user):
        response = api_client.get(BLOCKED_ORIGINS)
        assert response.status_code == 200
        assert len(response.content) == 0


def test_blocked_origin(api_client, fake_users):
    IP_ADDRESS = '192.168.1.1'
    user = fake_users()
    with api_client.auth(user=user):
        request_factory = RequestFactory()
        request = request_factory.get(LOGIN)
        request.META['REMOTE_ADDR'] = IP_ADDRESS
        assert defender.get_user_attempts(request, username=user.email) == 0

        response = api_client.get(BLOCKED_ORIGINS)
        assert response.status_code == 200
        assert len(response.content) == 0

        data = {
            'email': user.email,
            'password': 'wrong_password',
        }
        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 400
        assert defender.get_user_attempts(request, username=user.email) == 1
        assert IP_ADDRESS not in defender.get_blocked_ips()

        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 400
        assert defender.get_user_attempts(request, username=user.email) == 2
        assert IP_ADDRESS not in defender.get_blocked_ips()

        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 400
        assert defender.get_user_attempts(request, username=user.email) == 3
        assert IP_ADDRESS not in defender.get_blocked_ips()

        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 400
        assert defender.get_user_attempts(request, username=user.email) == 4
        assert IP_ADDRESS not in defender.get_blocked_ips()

        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 400
        assert defender.get_user_attempts(request, username=user.email) == 5
        assert IP_ADDRESS not in defender.get_blocked_ips()

        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 403
        assert defender.get_user_attempts(request, username=user.email) == 6
        assert IP_ADDRESS in defender.get_blocked_ips()

        response = api_client.get(BLOCKED_ORIGINS)
        assert response.status_code == 200
        assert len(response.content) == 1

        origin = response.content[0]
        assert 'ttl' in origin
        assert 'attempt_time' in origin
        assert 'ip_address' in origin and origin['ip_address'] == IP_ADDRESS

    REDIS_SERVER.flushdb()


def test_unblocked_origin(api_client, fake_users):
    IP_ADDRESS = '192.168.1.1'
    user = fake_users()
    with api_client.auth(user=user):
        # Register a failed attempt
        data = {
            'email': user.email,
            'password': 'wrong_password',
        }
        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 400
        # Block origin
        defender.block_ip(IP_ADDRESS)

        # Ensure block is propperly working
        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 403

        response = api_client.delete(BLOCKED_ORIGIN(IP_ADDRESS))
        assert response.status_code == 200

        # Test login again
        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 400

    REDIS_SERVER.flushdb()


def test_failed_unblock_origin(api_client, fake_users):
    IP_ADDRESS_1 = '192.168.1.1'
    IP_ADDRESS_2 = '192.168.1.2'
    user = fake_users()
    with api_client.auth(user=user):
        # Register a failed attempt
        data = {
            'email': user.email,
            'password': 'wrong_password',
        }
        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS_1)
        assert response.status_code == 400
        # Block origin
        defender.block_ip(IP_ADDRESS_1)
        defender.block_ip(IP_ADDRESS_2)

        # Ensure block is propperly working
        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS_1)
        assert response.status_code == 403

        # Invalid IP
        response = api_client.delete(BLOCKED_ORIGIN('192.168.1.300'))
        assert response.status_code == 400

        # IP not blocked
        response = api_client.delete(BLOCKED_ORIGIN('192.168.1.10'))
        assert response.status_code == 400

        # IP blocked, but no failed attempt
        response = api_client.delete(BLOCKED_ORIGIN(IP_ADDRESS_2))
        assert response.status_code == 400

        # Still blocked
        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS_1)
        assert response.status_code == 403

    REDIS_SERVER.flushdb()


def test_access_attempt_list(api_client, fake_users):
    user = fake_users()
    IP_ADDRESS = '192.168.1.1'
    with api_client.auth(user=user):
        response = api_client.get(ACCESS_ATTEMPTS)
        assert response.status_code == 200
        assert len(response.content) == 0

        # Register a failed attempt
        data = {
            'email': user.email,
            'password': 'wrong_password',
        }
        response = api_client.post(LOGIN, data, REMOTE_ADDR=IP_ADDRESS)
        assert response.status_code == 400

        response = api_client.get(ACCESS_ATTEMPTS)
        assert response.status_code == 200
        assert len(response.content) == 1
        assert response.content[0]['ip_address'] == IP_ADDRESS
