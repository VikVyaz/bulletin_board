import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    ROLE = [
        ("user", "Обычный пользователь"),
        ("admin", "Админ")
    ]

    MAILING_FREQ = [
        ('day', 'Ежедневная рассылка'),
        ('week', 'Еженедельная рассылка'),
        ('month', 'Ежемесячная рассылка')
    ]

    username = models.CharField(
        max_length=20,
        unique=True
    )
    first_name = models.CharField(
        verbose_name="Имя пользователя",
        help_text="Имя пользователя"
    )
    last_name = models.CharField(
        verbose_name="Фамилия пользователя",
        help_text="Фамилия пользователя"
    )
    phone = models.CharField(
        verbose_name="Номер телефона пользователя",
        help_text="Номер телефона пользователя"
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Email пользователя",
        help_text="Email пользователя"
    )
    role = models.CharField(
        verbose_name="Роль пользователя",
        choices=ROLE,
        default="user",
        help_text="Роль пользователя"
    )
    image = models.ImageField(
        verbose_name="Аватарка пользователя",
        upload_to="avatars/",
        default="default/user.png",
        help_text="Аватарка пользователя"
    )
    mailing = models.BooleanField(
        default=False,
        verbose_name='Статус рассылки о количестве новых отзывов под объявлениями пользователя',
        help_text='Статус рассылки о количестве новых отзывов под объявлениями пользователя'
    )
    mailing_frequency = models.CharField(
        choices=MAILING_FREQ,
        default='month',
        blank=True,
        null=True,
        verbose_name='Частота рассылки: день/неделя/месяц (Если рассылка активна | mailing=True)',
        help_text='Частота рассылки: день/неделя/месяц (Если рассылка активна | mailing=True)'
    )
    next_mailing = models.DateField(
        auto_now_add=True,
        verbose_name='Дата следующей рассылки (Если рассылка активна | mailing=True)',
        help_text='Дата следующей рассылки (Если рассылка активна | mailing=True)'
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Пользователь {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователь"
