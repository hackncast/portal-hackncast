import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def query_hibp(password):  # pragma: no cover
    response = requests.get(
        'https://api.pwnedpasswords.com/pwnedpassword/{}'.format(password)
    )
    if response.status_code == 200:
        count = response.json()
        return (True, count)
    return (False, None)


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
