from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from board.filters import AdFilter
from board.models import Ad, Feedback
from board.paginators import AdPaginator, FeedbackPaginator
from board.serializers import AdSerializer, FeedbackSerializer


class AdListView(generics.ListAPIView):
    serializer_class = AdSerializer
    pagination_class = AdPaginator

    def get_queryset(self):
        if self.request.user.role == "user":
            return Ad.objects.filter(is_public=True)
        return Ad.objects.all()


class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdRetrieveView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdUpdateView(generics.UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdDestroyView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class FeedbackListView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    pagination_class = FeedbackPaginator


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackRetrieveView(generics.RetrieveAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackUpdateView(generics.UpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackDestroyView(generics.DestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class SearchView(generics.ListAPIView):
    serializer_class = AdSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def get_base_queryset(self):
        if self.request.user.role == "user":
            return Ad.objects.filter(is_public=True)
        return Ad.objects.all()
