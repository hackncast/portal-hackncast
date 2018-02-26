#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.views.generic.base import RedirectView


class RedirectPasswordReset(RedirectView):
    permanent = False
    query_string = True
    pattern_name = 'article-detail'

    def get_redirect_url(self, uidb64, token, *args, **kwargs):
        return '/admin/#/user/password/reset/token/{}/{}/'.format(
            uidb64, token
        )
