from rest_framework import permissions


class IsModerator(permissions.BasePermission):
    """Проверка прав доступа для пользователей группы moderators."""
    message = 'Вы не относитесь к группе модераторов'

    def has_permission(self, request, view):
        """Проверяет, состоит ли пользователь в группе Moderator."""
        return request.user.groups.filter(name="moderators").exists()


class IsOwner(permissions.BasePermission):
    """Проверка прав доступа для владельцев."""

    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь владельцем."""
        return obj.owner == request.user
