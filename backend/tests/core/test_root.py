#!/usr/bin/env python3
# encoding: utf-8


def test_root(api_client, django_assert_num_queries):
    with django_assert_num_queries(0):
        response = api_client.get('/api/')
        assert response.status_code == 200
        assert type(response.content) == dict
        assert len([k for k in response.content.keys()]) > 1
        assert response.content['core'][0]['url'] == '/api/auth/login/'


def test_logged_in_root(api_client, django_assert_num_queries, fake_users):
    user = fake_users()
    with api_client.auth(user=user):
        response = api_client.get('/api/')
        assert response.status_code == 200
        assert type(response.content) == dict
        assert len([k for k in response.content.keys()]) > 1
