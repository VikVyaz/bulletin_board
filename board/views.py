from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from board.filters import AdFilter
from board.models import Ad, Feedback
from board.paginators import AdPaginator, FeedbackPaginator
from board.permissions import IsAdmin, IsAuthor
from board.serializers import AdSerializer, FeedbackSerializer


class AdListView(generics.ListAPIView):
    serializer_class = AdSerializer
    pagination_class = AdPaginator
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        if self.request.user.role == "user":
            return Ad.objects.filter(is_public=True)
        return Ad.objects.all()


class AdCreateView(generics.CreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdRetrieveView(generics.RetrieveAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdUpdateView(generics.UpdateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAdmin | IsAuthor]


class AdDestroyView(generics.DestroyAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAdmin | IsAuthor]


class FeedbackListView(generics.ListAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    pagination_class = FeedbackPaginator


class FeedbackCreateView(generics.CreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedbackRetrieveView(generics.RetrieveAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackUpdateView(generics.UpdateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdmin | IsAuthor]


class FeedbackDestroyView(generics.DestroyAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdmin | IsAuthor]


class SearchView(generics.ListAPIView):
    serializer_class = AdSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def get_base_queryset(self):
        if self.request.user.role == "user":
            return Ad.objects.filter(is_public=True)
        return Ad.objects.all()
