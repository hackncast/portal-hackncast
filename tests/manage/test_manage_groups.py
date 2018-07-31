#!/usr/bin/env python3
# encoding: utf-8

from django.urls import reverse
from django.contrib.auth.models import Group

from tests.utils import part_reverse, find_object

GROUPS = reverse('manage-group-list')
GROUP = part_reverse('manage-group-detail')
GROUP_USERS = part_reverse('manage-group-users')


def test_user_listing_fail(api_client, fake_users):
    user = fake_users()
    response = api_client.get(GROUPS)
    assert response.status_code == 403

    response = api_client.get(GROUP(1))
    assert response.status_code == 403

    response = api_client.get(GROUP_USERS(1))
    assert response.status_code == 403

    with api_client.auth(user=user):
        response = api_client.get(GROUPS)
        assert response.status_code == 403

        response = api_client.get(GROUP(1))
        assert response.status_code == 403

        response = api_client.get(GROUP_USERS(1))
        assert response.status_code == 403


def test_manage_group_listing(api_client, fake_users):
    user = fake_users(is_staff=True)
    with api_client.auth(user=user):
        response = api_client.get(GROUPS)
        assert response.status_code == 200
        assert len(response.content) == Group.objects.count()

        g = find_object(response.content, 'name', 'Core')
        assert g['pk'] == 1
        assert g['name'] == 'Core'
        assert len(g['users']) == 0


def test_manage_group_detail(api_client, fake_users):
    user = fake_users(is_staff=True)

    g = Group.objects.first()
    users = fake_users(3)
    g.user_set.set(users)
    g.save()

    with api_client.auth(user=user):
        response = api_client.get(GROUP(g.pk))
        assert response.status_code == 200
        assert response.content['name'] == g.name
        assert response.content['pk'] == g.pk
        assert len(response.content['users']) == 3

        user1 = users[0]
        u1 = find_object(response.content['users'], 'pk', user1.pk)
        assert user1.pk == u1['pk']
        assert user1.first_name == u1['first_name']
        assert user1.last_name == u1['last_name']
        assert user1.email == u1['email']
        assert user1.is_active == u1['is_active']
        assert user1.username == u1['username']


def test_manage_group_updating(api_client, fake_users):
    user = fake_users(is_staff=True)
    g = Group.objects.first()

    with api_client.auth(user=user):
        response = api_client.patch(GROUP(g.pk), {'name': 'Another Group'})
        assert response.status_code == 200

        response = api_client.get(GROUP(g.pk))
        assert response.status_code == 200
        assert response.content['name'] != g.name
        assert response.content['name'] == 'Another Group'
        assert response.content['pk'] == g.pk
        assert len(response.content['users']) == g.user_set.count()


def test_manage_group_users_patch(api_client, fake_users):
    user = fake_users(is_staff=True)
    users = fake_users(2)
    g = Group.objects.first()

    with api_client.auth(user=user):
        response = api_client.get(GROUP(g.pk))
        assert response.status_code == 200
        assert len(response.content['users']) == 0

        u = users[0]
        response = api_client.patch(GROUP_USERS(g.pk), u.pk)
        assert response.status_code == 200
        assert len(response.content['users']) == 1
        assert find_object(response.content['users'], 'pk', u.pk) is not None

        u = users[1]
        response = api_client.patch(GROUP_USERS(g.pk), [u.pk])
        assert response.status_code == 200
        assert len(response.content['users']) == 2
        assert find_object(response.content['users'], 'pk', u.pk) is not None


def test_manage_group_delete_users(api_client, fake_users):
    user = fake_users(is_staff=True)
    users = fake_users(3)

    g = Group.objects.first()
    g.user_set.set(users)
    g.save()

    with api_client.auth(user=user):
        response = api_client.get(GROUP(g.pk))
        assert response.status_code == 200
        assert len(response.content['users']) == 3

        response = api_client.delete(GROUP_USERS(g.pk), users[0].pk)
        assert response.status_code == 204
        response = api_client.get(GROUP(g.pk))
        assert response.status_code == 200
        assert len(response.content['users']) == 2

        response = api_client.delete(
            GROUP_USERS(g.pk), [users[1].pk, users[2].pk]
        )
        assert response.status_code == 204
        response = api_client.get(GROUP(g.pk))
        assert response.status_code == 200
        assert len(response.content['users']) == 0


def test_manage_group_delete_all_users(api_client, fake_users):
    user = fake_users(is_staff=True)
    users = fake_users(2)

    g = Group.objects.first()
    g.user_set.set(users)
    g.save()

    with api_client.auth(user=user):
        response = api_client.get(GROUP(g.pk))
        assert response.status_code == 200
        assert len(response.content['users']) == 2

        response = api_client.put(GROUP_USERS(g.pk), [])
        assert response.status_code == 200

        response = api_client.get(GROUP(g.pk))
        assert response.status_code == 200
        assert len(response.content['users']) == 0
