from rest_framework import permissions
from django.contrib.auth.models import Group


def is_in_group(user, group_name):
    """
    Takes a user and a group name, and returns `True` if the user is in that group.
    """
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


class IsCreator(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and is_in_group(request.user, "Creator"))


class IsAuthor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsNotAnonymousObjectOrPerformByAdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(bool(obj.user) or request.user.is_superuser)
