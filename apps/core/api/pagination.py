#!/usr/bin/env python
# -*- coding: utf-8 -*-

from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'size'
    max_page_size = 1000
