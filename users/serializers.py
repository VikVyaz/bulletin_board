from datetime import timedelta

from django.utils import timezone
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для User"""

    class Meta:
        model = User
        fields = (
            'username', 'password', 'first_name', 'last_name', 'phone',
            'email', 'role', 'image', 'mailing', 'mailing_frequency'
        )
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()

        frequency = {
            'day': timedelta(days=1),
            'week': timedelta(weeks=1),
            'month': timedelta(days=30)
        }

        insert_frequency = validated_data.get('mailing_frequency') or 'month'
        user.next_mailing = timezone.now().date() + frequency[insert_frequency]
        user.save()

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """Сериализатор только для UPDATE для User"""

    class Meta:
        model = User
        fields = (
            'username', 'password', 'first_name', 'last_name', 'phone',
            'email', 'role', 'image', 'mailing', 'mailing_frequency', 'next_mailing'
        )
        extra_kwargs = {"password": {"write_only": True}}

    def validate_next_mailing(self, value):
        if value < timezone.now().date():
            raise serializers.ValidationError("Next mailing date cannot be in the past")
        return value

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user


class PasswordResetRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса сброса пароля"""

    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Сериализатор для подтверждения сброса пароля на основе данных с почты"""

    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(max_length=15)
