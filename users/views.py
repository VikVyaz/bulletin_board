from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers import (PasswordResetConfirmSerializer,
                               PasswordResetRequestSerializer, UserSerializer)

from .tasks import send_reset_password_mail


class UserListAPIView(ListAPIView):
    """List view для User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserCreateAPIView(CreateAPIView):
    """Create view для User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny,)


class UserRetrieveAPIView(RetrieveAPIView):
    """Retrieve view для User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserUpdateAPIView(UpdateAPIView):
    """Update view для User"""

    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDestroyAPIView(DestroyAPIView):
    """Destroy view для User"""

    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class PasswordResetRequestAPIView(APIView):
    """APIView для запроса сброса пароля"""

    permissions_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = user.pk

            scheme = request.scheme
            domain = request.get_host()
            base_url = f"{scheme}://{domain}"

            reset_link = f"{base_url}/reset_password/{uid}/{token}"

            send_reset_password_mail.delay(user.email, reset_link)

        except User.DoesNotExist:
            pass

        return Response(
            {"message": "Если пользователь существует, письмо отправлено."},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        try:
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
            else:
                raise ValidationError

            return Response({"success": "Пароль изменен"}, status=status.HTTP_200_OK)

        except User.DoesNotExist or ValidationError:
            return Response(
                {"fail": "Неверный uid или token"}, status=status.HTTP_400_BAD_REQUEST
            )
