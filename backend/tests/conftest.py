#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest

from tests.factories import UserFactory, UserSessionFactory

from .utils import ApiClient


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture(scope='function')
def api_client():
    return ApiClient()


@pytest.fixture(scope='function')
def fake_users(db):
    def make_fake_users(count=1):
        if count == 1:
            return UserFactory()
        else:
            return UserFactory.create_batch(count)
    return make_fake_users


@pytest.fixture(scope='function')
def fake_user_sessions(db):
    def make_fake_user_sessions(user, count=1):
        if count == 1:
            return UserSessionFactory.create(user=user)
        else:
            return UserSessionFactory.create_batch(count, user=user)
    return make_fake_user_sessions
