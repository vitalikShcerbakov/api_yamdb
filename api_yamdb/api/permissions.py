from rest_framework import permissions
from users.models import User


class AuthorOrReadOnly(permissions.BasePermission):
    """Автор + доступ модератору, админу"""
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )


class IsAdminOrSuperUserOrReadOnly(permissions.BasePermission):
    """Разрешает добавлять и удалять объект,
       только если пользователь является администратором."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (
            request.user.is_authenticated and request.user.role == User.ADMIN
            or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == User.ADMIN
        )


class IsModerator(permissions.BasePermission):
    """Модератор"""
    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.role == User.ADMIN
            or request.user.is_superuser
            or request.user.role == User.MODERATOR
        )


class IsAdmimOrSuperUser(permissions.BasePermission):
    """Суперюзер всегда c правами пользователя admin.
    Суперюзер — всегда админ, админ — не обязательно суперюзер."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == User.ADMIN or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or request.user.role == User.ADMIN
