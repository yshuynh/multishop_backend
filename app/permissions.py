from rest_framework import permissions

from app.utils.constants import USER_ROLE


class AdminPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        return request.user.role == USER_ROLE.ADMIN


class UserPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        return request.user.role == USER_ROLE.User