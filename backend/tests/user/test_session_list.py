#!/usr/bin/env python3
# encoding: utf-8

from datetime import date
from django.urls import reverse

from ..utils import part_reverse

from qsessions.models import Session

SESSION = reverse('session-list')
SESSION_DETAIL = part_reverse('session-detail')


def test_permissions(api_client, fake_users):
    user = fake_users()
    response = api_client.get(SESSION)
    assert response.status_code == 403

    with api_client.auth(user=user):
        response = api_client.get(SESSION)
        assert response.status_code == 200


def test_session_list(api_client, fake_users, fake_user_sessions):
    user = fake_users()
    fake_user_sessions(user, count=3)

    with api_client.auth(user=user):
        response = api_client.get(SESSION)
        assert response.status_code == 200
        current = [item for item in response.content if item['current']]
        others = [item for item in response.content if not item['current']]
        assert len(response.content) == 4
        assert len(current) == 1
        assert len(others) == 3


def test_session_detail(api_client, fake_users):
    user = fake_users()
    today = date.today().isoformat()
    with api_client.auth(user=user):
        response = api_client.get(SESSION)
        pk = response.content[0]['pk']

        response = api_client.get(SESSION_DETAIL(pk))
        assert response.status_code == 200
        assert response.content['current'] is True
        assert response.content['updated_at'].startswith(today)


def test_session_segmentation(api_client, fake_users, fake_user_sessions):
    users = fake_users(2)
    sessions1 = fake_user_sessions(users[0], count=3)
    sessions2 = fake_user_sessions(users[1], count=5)

    sessions1_keys = [session.pk for session in sessions1]
    sessions2_keys = [session.pk for session in sessions2]

    assert Session.objects.count() == 8

    with api_client.auth(user=users[0]):
        response = api_client.get(SESSION)
        assert len(response.content) == 4
        for session in response.content:
            assert session['pk'] not in sessions2_keys

        for key in sessions2_keys:
            response = api_client.get(SESSION_DETAIL(key))
            assert response.status_code == 404

    with api_client.auth(user=users[1]):
        response = api_client.get(SESSION)
        assert len(response.content) == 6
        for session in response.content:
            assert session['pk'] not in sessions1_keys

        for key in sessions1_keys:
            response = api_client.get(SESSION_DETAIL(key))
            assert response.status_code == 404


def test_session_deletion(api_client, fake_users, fake_user_sessions):
    user = fake_users()
    fake_user_sessions(user, count=3)

    assert Session.objects.count() == 3

    with api_client.auth(user=user):
        response = api_client.get(SESSION)
        assert len(response.content) == 4
        others = [item for item in response.content if not item['current']]

        api_client.delete(SESSION_DETAIL(others[0]['pk']))
        assert Session.objects.count() == 3

        api_client.delete(SESSION_DETAIL(others[1]['pk']))
        assert Session.objects.count() == 2

        api_client.delete(SESSION_DETAIL(others[2]['pk']))
        assert Session.objects.count() == 1


def test_cant_delete_others_sessions(api_client, fake_users, fake_user_sessions):
    users = fake_users(2)
    sessions1 = fake_user_sessions(users[0], count=2)
    sessions2 = fake_user_sessions(users[1], count=2)

    sessions1_keys = [session.pk for session in sessions1]
    sessions2_keys = [session.pk for session in sessions2]

    assert Session.objects.count() == 4

    with api_client.auth(user=users[0]):
        for key in sessions2_keys:
            response = api_client.delete(SESSION_DETAIL(key))
            assert response.status_code == 404

    with api_client.auth(user=users[1]):
        for key in sessions1_keys:
            response = api_client.delete(SESSION_DETAIL(key))
            assert response.status_code == 404

    assert Session.objects.count() == 4
