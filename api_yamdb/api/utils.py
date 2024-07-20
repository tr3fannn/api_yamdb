from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from reviews.models import UserCustomRoles


def check_admin_permission(request):
    """
    Проверка прав доступа для администраторов.
    Возвращает None, если доступ разрешен,
    иначе возвращает Response с соответствующим статусом ошибки.
    """
    if not request.user.is_authenticated:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    if request.user.role in (
        UserCustomRoles.USER.value,
        UserCustomRoles.MODERATOR.value,
    ):
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
    if request.user != obj and request.user.role == UserCustomRoles.USER.value:
        raise PermissionDenied()
    return None
