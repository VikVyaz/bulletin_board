from django.contrib import admin

from board.models import Ad, Feedback


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    """Доступ для админки для PleasantHabit"""

    list_display = [field.name for field in Ad._meta.fields]


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    """Доступ для админки для PleasantHabit"""

    list_display = [field.name for field in Feedback._meta.fields]
