from rest_framework.pagination import PageNumberPagination

class DefaultPagaingation(PageNumberPagination):
    page_size = 10