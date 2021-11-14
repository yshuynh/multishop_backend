from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions

from app.models import NONE_USER
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
        return request.user.role == USER_ROLE.USER


class LoggedPermission(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        return request.user != NONE_USER and request.user != AnonymousUser


class OwnerCartPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
