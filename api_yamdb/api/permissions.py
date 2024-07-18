from rest_framework import permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response


class AdminOnlyExceptUpdateDestroy(permissions.BasePermission):
    """
    Пермишн для администраторов,
    позволяющий доступ к действиям, кроме обновления и удаления.
    """

    def has_permission(self, request, view):
        if request.method not in ['PATCH', 'DELETE']:
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.role == 'admin'
            )
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_superuser or request.user.role == 'admin'
        )


class IsOwnerOrModerOrAdmin(permissions.BasePermission):
    """
    Проверка пользователя на наличие прав владельца,
    модератора, администратора."""
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return True

    def has_object_permission(self, request, view, obj):
        if request.method not in permissions.SAFE_METHODS:
            return (request.user.is_authenticated
                    and (obj.author == request.user
                         or request.user.is_superuser
                         or request.user.role == 'admin'
                         or request.user.role == 'moderator'))
        return True


def check_admin_permission(request):
    """
    Проверка прав доступа для администраторов.
    Возвращает None, если доступ разрешен,
    иначе возвращает Response с соответствующим статусом ошибки.
    """
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.user.role in ('user', 'moderator'):
        return Response(status=status.HTTP_403_FORBIDDEN)
    return None


def check_authentication(request):
    """
    Проверка аутентификации пользователя.
    Возвращает Response со статусом 401, если пользователь не аутентифицирован.
    """
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    return None


def check_self_action(request, obj):
    """
    Проверка на выполнение действий самим пользователем.
    Возвращает Response со статусом 403,
    если пользователь пытается выполнить действие с другим пользователем.
    """
    if request.user != obj and request.user.role == 'user':
        raise PermissionDenied()
    return None
