from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    The access right is only for users with administrator right.
    """

    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.is_admin


class IsSuperuser(permissions.BasePermission):
    """
    The access right is only for superusers.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_superuser
