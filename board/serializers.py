from rest_framework import serializers

from board.models import Ad, Feedback
from users.serializers import UserSerializer


class FeedbackSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Mate:
        model = Feedback
        fields = "__all__"
        read_only_fields = ('author',)


class AdSerializer(serializers.ModelSerializer):
    feedbacks = FeedbackSerializer(many=True, read_only=True)
    author = UserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = "__all__"
        read_only_fields = ('author',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")

        if request:
            if request.user.role == "user":
                self.fields.pop("is_public", None)
