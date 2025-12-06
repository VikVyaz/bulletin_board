from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """Пермишен для пользователя с role == 'admin'"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAuthor(BasePermission):
    """Пермишен для автора объявления/отзыва"""

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
