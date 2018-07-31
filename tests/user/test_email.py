#!/usr/bin/env python3
# encoding: utf-8

from django.urls import reverse

from tests.utils import part_reverse
from tests.factories import EmailAddressFactory


USER = reverse('rest_user_details')
EMAILS = reverse('email-list')
EMAIL = part_reverse('email-detail')
EMAIL_PRIMARY = reverse('email-primary')
RESEND_EMAIL = part_reverse('email-resend')


def test_unauthorized_email_listing(api_client):
    response = api_client.get(EMAILS)
    assert response.status_code == 403

    response = api_client.get(EMAIL(123))
    assert response.status_code == 403

    response = api_client.get(RESEND_EMAIL(123))
    assert response.status_code == 403


def test_successfull_email_listing(api_client, fake_users):
    user = fake_users()
    with api_client.auth(user=user):
        response = api_client.get(USER)
        assert response.status_code == 200

        response = api_client.get(EMAILS)
        assert response.status_code == 200
        assert len(response.content) == 1

    EmailAddressFactory.create(user=user, email="new_email_1@teste.com")
    EmailAddressFactory.create(user=user, email="new_email_2@teste.com")
    EmailAddressFactory.create(user=user, email="new_email_3@teste.com")

    with api_client.auth(user=user):
        response = api_client.get(EMAILS)
        assert response.status_code == 200
        assert len(response.content) == 4


def test_successfull_email_detail(api_client, fake_users):
    user = fake_users()
    primary_email = user.emailaddress_set.get(primary=True)
    e1 = EmailAddressFactory.create(user=user, email="new_email_1@teste.com")

    with api_client.auth(user=user):
        response = api_client.get(EMAIL(primary_email.pk))
        assert response.status_code == 200
        assert response.content['email'] == primary_email.email

        response = api_client.get(EMAIL(e1.pk))
        assert response.status_code == 200
        assert response.content['email'] == e1.email

        response = api_client.get(EMAIL(e1.pk + 1))
        assert response.status_code == 404


def test_new_email_validation(api_client, fake_users):
    user = fake_users()

    with api_client.auth(user=user):
        response = api_client.get(EMAILS)
        assert response.status_code == 200
        assert len(response.content) == 1

        # Empty email
        response = api_client.post(EMAILS, {'email': ''})
        assert response.status_code == 400
        assert user.emailaddress_set.count() == 1

        # Invalid email
        response = api_client.post(EMAILS, {'email': 'not an email'})
        assert response.status_code == 400
        assert user.emailaddress_set.count() == 1

        # Duplicated email
        response = api_client.post(EMAILS, {'email': user.email})
        assert response.status_code == 400
        assert user.emailaddress_set.count() == 1


def test_new_email(api_client, fake_users, mailoutbox):
    user = fake_users()
    assert len(mailoutbox) == 0
    assert user.emailaddress_set.count() == 1

    with api_client.auth(user=user):
        response = api_client.post(EMAILS, {'email': 'new_email@test.com'})
        assert response.status_code == 201
        assert user.emailaddress_set.count() == 2
        assert len(mailoutbox) == 1

        response = api_client.post(
            EMAILS, {'email': 'another_new_email@test.com'}
        )
        assert response.status_code == 201
        assert user.emailaddress_set.count() == 3
        assert len(mailoutbox) == 2


def test_email_exclusion(api_client, fake_users):
    user = fake_users()

    e1 = EmailAddressFactory.create(user=user, email="new_email_1@teste.com")
    e2 = EmailAddressFactory.create(user=user, email="new_email_2@teste.com")
    e3 = EmailAddressFactory.create(user=user, email="new_email_3@teste.com")

    with api_client.auth(user=user):
        response = api_client.get(EMAILS)
        assert response.status_code == 200
        assert len(response.content) == 4

        response = api_client.delete(EMAIL(e1.pk))
        assert response.status_code == 204
        assert user.emailaddress_set.count() == 3

        response = api_client.delete(EMAIL(e2.pk))
        assert response.status_code == 204
        assert user.emailaddress_set.count() == 2

        response = api_client.delete(EMAIL(e3.pk))
        assert response.status_code == 204
        assert user.emailaddress_set.count() == 1


def test_primary_email_exclusion(api_client, fake_users):
    user = fake_users()
    EmailAddressFactory.create(user=user, email="new_email_1@teste.com")

    with api_client.auth(user=user):
        primary_email = user.emailaddress_set.get(primary=True)
        response = api_client.delete(EMAIL(primary_email.pk))
        assert response.status_code == 400
        assert user.emailaddress_set.count() == 2


def test_inexistent_email_exclusion(api_client, fake_users):
    user = fake_users()
    primary_email = user.emailaddress_set.get(primary=True)
    inexistent_pk = primary_email.pk + 1

    with api_client.auth(user=user):
        response = api_client.delete(EMAIL(inexistent_pk))
        assert response.status_code == 404


def test_resend_email_confirmation(api_client, fake_users, mailoutbox):
    user = fake_users()
    primary_email = user.emailaddress_set.get(primary=True)
    e1 = EmailAddressFactory.create(user=user, email="new_email_1@teste.com")
    assert len(mailoutbox) == 0

    with api_client.auth(user=user):
        response = api_client.post(RESEND_EMAIL(primary_email.pk), {})
        assert response.status_code == 200
        assert len(mailoutbox) == 1

        response = api_client.post(RESEND_EMAIL(e1.pk), {})
        assert response.status_code == 200
        assert len(mailoutbox) == 2


def test_resend_inexistent_email_confirmation(api_client, fake_users,
                                              mailoutbox):
    user = fake_users()
    primary_email = user.emailaddress_set.get(primary=True)
    inexistent_pk = primary_email.pk + 1
    assert len(mailoutbox) == 0

    with api_client.auth(user=user):
        response = api_client.post(RESEND_EMAIL(inexistent_pk), {})
        assert response.status_code == 404
        assert len(mailoutbox) == 0


def test_get_primary_email(api_client, fake_users):
    user = fake_users()
    primary = user.emailaddress_set.get(primary=True)
    with api_client.auth(user=user):
        response = api_client.get(EMAIL_PRIMARY)
        assert response.status_code == 200
        assert 'email' in response.content
        assert 'pk' in response.content
        assert 'verified' in response.content
        assert 'primary' in response.content

        assert response.content['pk'] == primary.pk
        assert response.content['email'] == primary.email
        assert response.content['primary'] is True
        assert response.content['verified'] is False


def test_change_primary_email(api_client, fake_users):
    user = fake_users()
    primary_email = user.emailaddress_set.get(primary=True)
    primary_email.verified = True
    primary_email.save()
    e1 = EmailAddressFactory.create(
        user=user, email="new_email_1@teste.com", verified=True,
    )
    assert user.emailaddress_set.filter(verified=True).count() == 2

    with api_client.auth(user=user):
        response = api_client.post(EMAIL_PRIMARY, {'pk': e1.pk})
        assert response.status_code == 200

        e1.refresh_from_db()
        primary_email.refresh_from_db()
        assert primary_email.primary is False
        assert e1.primary is True

        response = api_client.post(EMAIL_PRIMARY, {'pk': primary_email.pk})
        assert response.status_code == 200

        e1.refresh_from_db()
        primary_email.refresh_from_db()
        assert primary_email.primary is True
        assert e1.primary is False


def test_change_primary_email_unverified(api_client, fake_users):
    user = fake_users()
    primary_email = user.emailaddress_set.get(primary=True)
    primary_email.verified = True
    primary_email.save()
    e1 = EmailAddressFactory.create(user=user, email="new_email_1@teste.com")

    with api_client.auth(user=user):
        response = api_client.post(EMAIL_PRIMARY, {'pk': e1.pk})
        assert response.status_code == 400

        e1.refresh_from_db()
        primary_email.refresh_from_db()
        assert primary_email.primary is True
        assert e1.primary is False

        response = api_client.post(EMAIL_PRIMARY, {'pk': primary_email.pk})
        assert response.status_code == 200

        e1.refresh_from_db()
        primary_email.refresh_from_db()
        assert primary_email.primary is True
        assert e1.primary is False


def test_change_primary_inexistent_email(api_client, fake_users):
    user = fake_users()
    primary_email = user.emailaddress_set.get(primary=True)
    inexistent_pk = primary_email.pk + 1

    with api_client.auth(user=user):
        response = api_client.post(EMAIL_PRIMARY, {'pk': inexistent_pk})
        assert response.status_code == 404
