from celery import shared_task
from django.core.mail import send_mail
import logging

from config import settings


@shared_task
def send_notification(user_from, email_to, ad_title):

    try:
        send_mail(
            subject="Новый отзыв",
            message=f"Пользователь {user_from} только что оставил новый отзыв под Вашим объявлением '{ad_title}'.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_to],
        )
    except Exception as e:
        logging.error(f'Ошибка отправки email: {e}')
        return False

    return True
