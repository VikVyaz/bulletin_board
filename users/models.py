from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель пользователя"""

    ROLE = [("user", "Обычный пользователь"), ("admin", "Админ")]

    first_name = models.CharField(
        verbose_name="Имя пользователя", help_text="Имя пользователя"
    )
    last_name = models.CharField(
        verbose_name="Фамилия пользователя", help_text="Фамилия пользователя"
    )
    phone = models.CharField(
        verbose_name="Номер телефона пользователя",
        help_text="Номер телефона пользователя",
    )
    email = models.EmailField(
        verbose_name="Email пользователя", unique=True, help_text="Email пользователя"
    )
    role = models.CharField(
        verbose_name="Роль пользователя",
        choices=ROLE,
        default="user",
        help_text="Роль пользователя",
    )
    image = models.ImageField(
        verbose_name="Аватарка пользователя",
        upload_to="avatars/",
        default="default/user.png",
        help_text="Аватарка пользователя",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"Пользователь {self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Пользователи"
        verbose_name_plural = "Пользователь"
