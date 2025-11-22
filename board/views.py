from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny
from board.filters import AdFilter
from board.models import Ad, Feedback
from board.paginators import AdPaginator, FeedbackPaginator
from board.permissions import IsAdmin, IsAuthor
from board.serializers import AdSerializer, FeedbackSerializer, AdCreateUpdateSerializer, FeedbackCreateUpdateSerializer


class AdListView(generics.ListAPIView):
    """List view для объявления"""

    serializer_class = AdSerializer
    pagination_class = AdPaginator
    permission_classes = [AllowAny]

    def get_queryset(self):
        if self.request.user.is_authenticated and self.request.user.role == "user":
            return Ad.objects.filter(is_public=True)
        return Ad.objects.all()


class AdCreateView(generics.CreateAPIView):
    """Create view для объявления"""

    queryset = Ad.objects.all()
    serializer_class = AdCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class AdRetrieveView(generics.RetrieveAPIView):
    """Retrieve view для объявления"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer


class AdUpdateView(generics.UpdateAPIView):
    """Update view для объявления"""

    queryset = Ad.objects.all()
    serializer_class = AdCreateUpdateSerializer
    permission_classes = [IsAdmin | IsAuthor]


class AdDestroyView(generics.DestroyAPIView):
    """Destroy view для объявления"""

    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = [IsAdmin | IsAuthor]


class FeedbackListView(generics.ListAPIView):
    """List view для отзыва"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    pagination_class = FeedbackPaginator


class FeedbackCreateView(generics.CreateAPIView):
    """Create view для отзыва"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FeedbackRetrieveView(generics.RetrieveAPIView):
    """Retrieve view для отзыва"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackUpdateView(generics.UpdateAPIView):
    """Update view для отзыва"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackCreateUpdateSerializer
    permission_classes = [IsAdmin | IsAuthor]


class FeedbackDestroyView(generics.DestroyAPIView):
    """Destroy view для отзыва"""

    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAdmin | IsAuthor]


class SearchView(generics.ListAPIView):
    """View для поиска по объявлениям"""

    serializer_class = AdSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AdFilter

    def get_queryset(self):
        if self.request.user.role == "user":
            return Ad.objects.filter(is_public=True)
        return Ad.objects.all()
