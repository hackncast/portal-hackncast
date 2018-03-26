import functools

from django.conf import settings

from rest_framework import exceptions
from defender import utils


def lockout_response():
    msg = "Congratulations, after too many failed attempts you're " +\
        "officially locked out! Please try again later or try from a " +\
        "different origin."
    raise exceptions.AuthenticationFailed(msg)


def watch_login(status_code=302, msg=''):
    def decorated_login(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            username = request.data.get(
                settings.DEFENDER_USERNAME_FORM_FIELD, None
            )
            if utils.is_already_locked(request._request, username=username):
                return lockout_response()

            exception = None
            try:
                response = func(request, *args, **kwargs)
            except Exception as e:
                exception = e

            login_valid = exception is None

            utils.add_login_attempt_to_db(
                request._request, login_valid=login_valid, username=username
            )

            if utils.check_request(request,
                                   login_unsuccessful=(not login_valid),
                                   username=username):
                if exception:
                    raise exception
                return response
            return lockout_response()
        return wrapper
    return decorated_login
