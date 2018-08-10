from collections import OrderedDict

import django
from django.urls import get_urlconf, get_resolver

if django.VERSION >= (2, 0):  # pragma: no cover
    from django.urls import URLResolver
else:  # pragma: no cover
    try:
        from django.urls import RegexURLResolver
    except ImportError:
        from django.core.urlresolvers import RegexURLResolver
    URLResolver = RegexURLResolver

APP_BLACK_LIST = ['silk']
URL_BLACK_LIST = ['root', 'password_reset_confirm', 'account_confirm_email']
TRANSLATE = {
    'core': {
        'restLogin': 'login',
        'restLogout': 'logout',
        'restPasswordChange': 'passwordChange',
        'restPasswordReset': 'passwordReset',
        'restPasswordResetConfirm': 'passwordResetConfirm',
        'restRegister': 'register',
        'restUserDetails': 'userDetails',
        'restVerifyEmail': 'verifyEmail',
    }
}


def __getUrlsFromApp(resolver, translator):  # pragma: no cover
    urls = []
    root = resolver.pattern.describe()\
        .replace("'", "").replace("^", "").replace("$", "")

    if not root.startswith('/'):
        root = '/' + root

    for pattern in resolver.url_patterns:
        if pattern.name in URL_BLACK_LIST:
            continue

        data = OrderedDict()
        name = pattern.name.split('-')
        name = [name[0]] + [n.capitalize() for n in name[1:]]
        name = ''.join(name)

        name = name.split('_')
        name = [name[0]] + [n.capitalize() for n in name[1:]]
        name = ''.join(name)

        if name in translator:
            data['name'] = translator[name]
        else:
            data['name'] = name

        url, args = resolver.reverse_dict[pattern.name][0][0]

        args = {arg: '{/%s}' % arg for arg in args}
        url = url % args
        data['url'] = root + url

        try:
            methods = pattern.callback.cls().allowed_methods
        except AttributeError:
            methods = None

        if methods:
            data['methods'] = methods

        urls.append(data)
    urls.sort(key=lambda x: x['name'])
    return urls


def getUrls():  # pragma: no cover
    urls = OrderedDict()
    resolver = get_resolver(get_urlconf())
    for app_resolver in resolver.url_patterns:
        if not isinstance(app_resolver, URLResolver):
            continue

        app = app_resolver.urlconf_name.__name__
        if app.startswith('modules'):
            app_name = app.split('.')[1]
        else:
            app_name = app.split('.')[0]

        if app_name in APP_BLACK_LIST:
            continue

        url_list = __getUrlsFromApp(
            app_resolver, TRANSLATE.get(app_name, dict())
        )

        if url_list:
            urls[app_name] = url_list

    return urls
