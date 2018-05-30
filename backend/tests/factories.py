#!/usr/bin/env python3
# encoding: utf-8

from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import get_user_model

import factory
import factory.fuzzy

from faker import Faker
from qsessions.models import Session
from factory.django import DjangoModelFactory

now = timezone.now()
faker = Faker()
User = get_user_model()
DEFAULT_PASSWORD = "password"


class UserFactory(DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.PostGenerationMethodCall('set_password',
                                                DEFAULT_PASSWORD)

    @factory.lazy_attribute
    def username(self):
        return '{}_{}'.format(
            self.first_name.replace(' ', '_'),
            self.last_name.replace(' ', '_'),
        ).lower()

    @factory.lazy_attribute
    def email(self):
        return '{}.{}@example.com'.format(
            self.first_name.replace(' ', '_'),
            self.last_name.replace(' ', '_'),
        ).lower()

    class Meta:
        model = User


class UserSessionFactory(DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    session_key = factory.Faker('md5', raw_output=False)
    user_agent = factory.Faker('user_agent')
    ip = factory.Faker('ipv4')
    updated_at = factory.fuzzy.FuzzyDateTime(
        start_dt=(now - timedelta(days=7)), end_dt=(now - timedelta(days=3)),
    )
    created_at = factory.fuzzy.FuzzyDateTime(
        start_dt=(now - timedelta(days=2)), end_dt=now,
    )
    expire_date = factory.fuzzy.FuzzyDateTime(
        start_dt=(now + timedelta(days=1)), end_dt=(now + timedelta(days=7)),
    )
    session_data = ''

    class Meta:
        model = Session
