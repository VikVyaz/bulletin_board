from rest_framework import serializers

from board.models import Ad, Feedback


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        request = self.context.get("request")

        if request:
            if request.user.role == "user":
                self.fields.pop("is_public", None)


class FeedbackSerializer(serializers.ModelSerializer):
    class Mate:
        model = Feedback
        fields = "__all__"
