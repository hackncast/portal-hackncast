#!/usr/bin/env python3
# encoding: utf-8

from django.urls import reverse
from django.contrib.auth.models import Group

from tests.utils import part_reverse, find_object, date_format


USERS = reverse('manage-user-list')
USER = part_reverse('manage-user-detail')
USER_GROUPS = part_reverse('manage-user-groups')


def test_gropu_listing_fail(api_client, fake_users):
    user = fake_users()
    response = api_client.get(USERS)
    assert response.status_code == 403

    response = api_client.get(USER(1))
    assert response.status_code == 403

    response = api_client.get(USER_GROUPS(1))
    assert response.status_code == 403

    with api_client.auth(user=user):
        response = api_client.get(USERS)
        assert response.status_code == 403

        response = api_client.get(USER(1))
        assert response.status_code == 403

        response = api_client.get(USER_GROUPS(1))
        assert response.status_code == 403


def test_manage_user_listing_basic_info(api_client, fake_users):
    user = fake_users(is_staff=True)
    with api_client.auth(user=user):
        response = api_client.get(USERS)
        assert response.status_code == 200
        assert response.content['count'] == 1
        u = response.content['results'][0]
        assert u['pk'] == user.pk
        assert u['username'] == user.username
        assert u['first_name'] == user.first_name
        assert u['last_name'] == user.last_name
        assert u['email'] == user.email
        assert u['is_active'] == user.is_active
        assert u['date_joined'] == date_format(user.date_joined)
        assert u['groups'] == []


def test_manage_user_listing_is_active(api_client, fake_users):
    user = fake_users(is_staff=True)

    inactive_user = fake_users()
    inactive_user.is_active = False
    inactive_user.save()

    with api_client.auth(user=user):
        response = api_client.get(USERS)
        assert response.status_code == 200
        assert response.content['count'] == 2
        results = response.content['results']

        other = find_object(results, 'pk', user.pk)
        assert other is not None
        assert other['is_active'] is True

        inactive = find_object(results, 'pk', inactive_user.pk)
        assert inactive is not None
        assert inactive['is_active'] is False


def test_manage_user_listing_groups(api_client, fake_users):
    user = fake_users(is_staff=True)
    other_users = fake_users(2)
    groups = [Group.objects.create(name=name) for name in ['g1', 'g2']]

    single_group_u = other_users[0]
    single_group_u.groups.add(groups[0])
    single_group_u.save()

    multi_group_u = other_users[1]
    multi_group_u.groups.add(groups[0])
    multi_group_u.groups.add(groups[1])
    multi_group_u.save()

    with api_client.auth(user=user):
        response = api_client.get(USERS)
        assert response.status_code == 200
        assert response.content['count'] == 3
        results = response.content['results']

        single_group = find_object(results, 'pk', single_group_u.pk)
        assert len(single_group['groups']) == 1
        assert single_group['groups'][0]['pk'] == groups[0].pk
        assert single_group['groups'][0]['name'] == groups[0].name

        multi_group = find_object(results, 'pk', multi_group_u.pk)
        assert len(multi_group['groups']) == 2
        assert multi_group['groups'][0]['pk'] == groups[0].pk
        assert multi_group['groups'][0]['name'] == groups[0].name
        assert multi_group['groups'][1]['pk'] == groups[1].pk
        assert multi_group['groups'][1]['name'] == groups[1].name


def test_manage_user_detail_sessions(api_client, fake_users):
    user = fake_users(is_staff=True)
    with api_client.auth(user=user):
        response = api_client.get(USER(user.pk))
        assert response.status_code == 200
        assert response.content['pk'] == user.pk
        assert response.content['username'] == user.username
        assert response.content['first_name'] == user.first_name
        assert response.content['last_name'] == user.last_name
        assert response.content['email'] == user.email
        assert response.content['is_active'] == user.is_active
        assert response.content['date_joined'] == date_format(user.date_joined)
        assert response.content['groups'] == []


def test_manage_user_partial_update_success(api_client, fake_users):
    user = fake_users(is_staff=True)
    other_user = fake_users()
    with api_client.auth(user=user):
        response = api_client.patch(
            USER(other_user.pk),
            {'is_active': False},
        )
        assert response.status_code == 200

        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert response.content['is_active'] is False
        assert response.content['is_staff'] is False

        response = api_client.patch(
            USER(other_user.pk),
            {'is_staff': True},
        )
        assert response.status_code == 200

        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert response.content['is_staff'] is True


def test_manage_user_partial_update_failure(api_client, fake_users):
    user = fake_users(is_staff=True)
    other_user = fake_users()
    with api_client.auth(user=user):
        response = api_client.patch(
            USER(other_user.pk),
            {'first_name': 'Some Random First Name'},
        )
        assert response.status_code == 200

        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert response.content['first_name'] == other_user.first_name


def test_manage_user_update_groups(api_client, fake_users):
    user = fake_users(is_staff=True)
    other_user = fake_users()

    group1 = Group.objects.create(name='group1')
    group2 = Group.objects.create(name='group2')

    with api_client.auth(user=user):
        response = api_client.patch(USER_GROUPS(other_user.pk), [])
        assert response.status_code == 204

        response = api_client.patch(USER_GROUPS(other_user.pk), group1.pk)
        assert response.status_code == 200

        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert response.content['groups'] == [
            {'pk': group1.pk, 'name': group1.name}
        ]

        response = api_client.patch(
            USER_GROUPS(other_user.pk), [group1.pk, group2.pk],
        )
        assert response.status_code == 200
        assert 'groups' in response.content
        assert len(response.content['groups']) == 2

        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert len(response.content['groups']) == 2
        pks = [group['pk'] for group in response.content['groups']]
        assert set(pks) == set([group1.pk, group2.pk])

        response = api_client.put(USER_GROUPS(other_user.pk), [])
        assert response.status_code == 200
        assert 'groups' in response.content
        assert len(response.content['groups']) == 0

        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert len(response.content['groups']) == 0


def test_manage_user_delete_groups(api_client, fake_users):
    user = fake_users(is_staff=True)
    other_user = fake_users()

    g1 = Group.objects.create(name='group1')
    other_user.groups.add(g1)
    g2 = Group.objects.create(name='group2')
    other_user.groups.add(g2)
    g3 = Group.objects.create(name='group3')
    other_user.groups.add(g3)

    other_user.save()

    with api_client.auth(user=user):
        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert len(response.content['groups']) == 3

        response = api_client.delete(
            USER_GROUPS(other_user.pk), g1.pk
        )
        assert response.status_code == 204
        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert len(response.content['groups']) == 2

        response = api_client.delete(
            USER_GROUPS(other_user.pk), [g2.pk, g3.pk]
        )
        assert response.status_code == 204
        response = api_client.get(USER(other_user.pk))
        assert response.status_code == 200
        assert len(response.content['groups']) == 0
