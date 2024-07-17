from rest_framework import permissions


class AdminOnlyExceptUpdateDestroy(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in ['PATCH', 'DELETE']:
            return (request.user.is_authenticated
                    and (request.user.is_superuser
                         or request.user.role == 'admin'))
        return True

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and (request.user.is_superuser
                     or request.user.role == 'admin'))