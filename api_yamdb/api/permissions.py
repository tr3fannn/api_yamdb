from http import HTTPMethod

from rest_framework import permissions
from reviews.models import UserCustomRoles


class AdminOnlyExceptUpdateDestroy(permissions.BasePermission):
    """
    Пермишн для администраторов,
    позволяющий доступ к действиям, кроме обновления и удаления.
    """

    def has_permission(self, request, view):
        if request.method not in [HTTPMethod.PATCH, HTTPMethod.DELETE]:
            return request.user.is_authenticated and (
                request.user.is_superuser
                or request.user.role == UserCustomRoles.ADMIN.value
            )
        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.role == UserCustomRoles.ADMIN.value
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
            return request.user.is_authenticated and (
                obj.author == request.user
                or request.user.is_superuser
                or request.user.role == UserCustomRoles.ADMIN.value
                or request.user.role == UserCustomRoles.MODERATOR.value
            )
        return True
