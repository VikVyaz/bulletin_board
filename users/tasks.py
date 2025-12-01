import logging
from datetime import timedelta

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from board.models import Feedback
from config import settings
from users.models import User


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
        logging.error(f'Ошибка отправки email: {e}')
        return False

    return True


@shared_task
def feedback_quantity_notification():
    users = User.objects.filter(mailing=True)
    today = timezone.now().date()

    frequency = {
        'day': ['день', timedelta(days=1)],
        'week': ['неделю', timedelta(weeks=1)],
        'month': ['месяц', timedelta(days=30)]
    }

    if users:
        for user in users:
            if user.next_mailing == today:
                unreported_feedbacks = Feedback.objects.filter(related_ad__author=user, reported_by_mail=False)

                if unreported_feedbacks.count():
                    msg = (f'было {unreported_feedbacks.count()} новых отзывов под твоими объявлениями.'
                           f'Скорее глянь на них!')
                else:
                    msg = f'не было новых отзывов под твоими объявлениями.'

                send_mail(
                    subject=f"Отчет за {frequency[user.mailing_frequency][0]}",
                    message=f"За это время {msg}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                )

                unreported_feedbacks.update(reported_by_mail=True)

                user.next_mailing = timezone.now() + frequency[user.mailing_frequency][1]
                user.save(update_fields=['next_mailing'])
