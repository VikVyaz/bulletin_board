from rest_framework.pagination import PageNumberPagination


class AdPaginator(PageNumberPagination):
    """Пагинатор дял объявлений"""

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 4


class FeedbackPaginator(PageNumberPagination):
    """Пагинатор для отзывов"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 5
