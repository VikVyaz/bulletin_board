from rest_framework import serializers

from board.models import Ad, Feedback
from users.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    """Сериализотор list/retrieve для отзыва"""

    author = UserSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ('author',)


class FeedbackCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор create/update для отзыва"""

    class Meta:
        model = Feedback
        fields = ['text', 'related_ad']


class AdSerializer(serializers.ModelSerializer):
    """Сериализатор list/retrieve для объявления"""

    feedbacks = FeedbackSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = "__all__"


class AdCreateUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор create/update для объявления"""

    class Meta:
        model = Ad
        fields = ['title', 'price', 'description']
