#!/usr/bin/env python3
# encoding: utf-8

from django.contrib.auth import get_user_model

import factory
from factory.django import DjangoModelFactory

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
