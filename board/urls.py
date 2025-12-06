from django.urls import path

from board.apps import BoardConfig

from .views import (AdCreateView, AdDestroyView, AdListView, AdRetrieveView,
                    AdUpdateView, FeedbackCreateView, FeedbackDestroyView,
                    FeedbackListView, FeedbackRetrieveView, FeedbackUpdateView,
                    SearchView)

app_name = BoardConfig.name


urlpatterns = [
    path("ads/list/", AdListView.as_view(), name="ad_list"),
    path("ads/create/", AdCreateView.as_view(), name="ad_create"),
    path("ads/details/<int:pk>/", AdRetrieveView.as_view(), name="ad_detail"),
    path("ads/update/<int:pk>/", AdUpdateView.as_view(), name="ad_update"),
    path("ads/delete/<int:pk>/", AdDestroyView.as_view(), name="ad_delete"),

    path("feedback/list/", FeedbackListView.as_view(), name="feedback_list"),
    path("feedback/create/", FeedbackCreateView.as_view(), name="feedback_create"),
    path("feedback/details/<int:pk>/", FeedbackRetrieveView.as_view(), name="feedback_detail"),
    path("feedback/update/<int:pk>", FeedbackUpdateView.as_view(), name="feedback_update"),
    path("feedback/delete/<int:pk>", FeedbackDestroyView.as_view(), name="feedback_delete"),

    path("search/", SearchView.as_view(), name="search"),
]
