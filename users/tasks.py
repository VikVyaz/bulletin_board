from celery import shared_task
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.response import Response

from config import settings


@shared_task
def send_reset_password_mail(email: str, link: str):
    """Asinc отправка письма на reset пароля"""

    try:
        send_mail(
            subject="Сброс пароля",
            message=f"Чтобы сбросить пароля перейдите по ссылке: {link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
    except Exception as e:
        return Response(
            {"error": f"Некорректный email.\n(Ошибка:{e})"},
            status=status.HTTP_400_BAD_REQUEST,
        )
