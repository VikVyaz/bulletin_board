from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Все поля модели
    list_display = ["email", "role", "is_staff", "is_superuser"]
