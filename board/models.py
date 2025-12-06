from django.db import models

from users.models import User


class Ad(models.Model):
    """Модель для Объявления"""

    title = models.CharField(
        max_length=20,
        verbose_name="Название товара",
        help_text="Название товара"
    )
    price = models.PositiveIntegerField(
        verbose_name="Цена товара",
        help_text="Цена товара"
    )
    description = models.TextField(
        max_length=200,
        verbose_name="Описание товара",
        help_text="Описание товара"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Автор объявления",
        help_text="Автор объявления",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания объявления",
        help_text="Дата и время создания объявления",
    )

    def __str__(self):
        return f'Объявление №{self.pk} - "{self.title}"'

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ["-created_at"]


class Feedback(models.Model):
    """Модель для Отзыва"""

    text = models.TextField(
        max_length=150,
        verbose_name="Текст отзыва",
        help_text="Текст отзыва"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Автор отзыва",
        help_text="Автор отзыва",
    )
    related_ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name="Объявление, под которым оставлен отзыв",
        help_text="Объявление, под которым оставлен отзыв",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания отзыва",
        help_text="Дата и время создания отзыва",
    )
    reported_by_mail = models.BooleanField(
        default=False,
        verbose_name='Статус осведомленности пользователя о новом отзыве под его объявлением',
        help_text='Статус осведомленности пользователя о новом отзыве под его объявлением'
    )

    def __str__(self):
        return f"Отзыв №{self.pk} на объявление № {self.related_ad.pk if self.related_ad else 'Отсутствует'}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
