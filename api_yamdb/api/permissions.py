from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Разрешает добавлять и удалять объект,
       только если пользователь является администратором."""
    def has_object_permission(self, request, view, obj):
        return (
            view.method in permissions.SAFE_METHODS
            or request.user.is_staff
        )
