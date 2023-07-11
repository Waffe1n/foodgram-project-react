from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    '''Common pagination with item amount 'limit' query param.'''
    page_size_query_param = 'limit'
