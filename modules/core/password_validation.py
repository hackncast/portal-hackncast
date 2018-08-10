#!/usr/bin/env python3
# encoding: utf-8

import requests
from hashlib import sha1

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def query_hibp(password):  # pragma: no cover
    hash = sha1(password.encode()).hexdigest().upper()
    (hpt1, hpt2) = (hash[:5], hash[5:])

    response = requests.get(
        'https://api.pwnedpasswords.com/range/{}'.format(hpt1)
    )
    if response.status_code != 200:
        return (False, None)

    matches = [i.split(':')
               for i in response.text.split()
               if i.startswith(hpt2)]

    if len(matches) == 0:
        return (False, None)

    return (True, int(matches[0][1]))


class HaveIBeenPwned:
    def validate(self, password, user=None):
        (success, count) = query_hibp(password)

        if success:
            quantifier = 'times' if count > 1 else 'time'
            raise ValidationError(
                _("Bitch please, this password has been pwned {} {}!").format(
                    count, quantifier
                ),
                code='password_too_common',
            )

    def get_help_text(self):  # pragma: no cover
        return "Your password must be secure and not Pwned!"
