#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination


class DefaultPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('page', self.page.number),
            ('num_pages', self.page.paginator.num_pages),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))

    def paginate_queryset(self, queryset, request, view=None):
        sort_by = request.GET.get('sort', None)
        descending = request.GET.get('descending', 'false') == 'true'

        if descending and sort_by:
            sort_by = '-' + sort_by

        if sort_by:
            queryset = queryset.order_by(sort_by)
        else:
            queryset.order_by('pk')

        return super().paginate_queryset(queryset, request, view)
