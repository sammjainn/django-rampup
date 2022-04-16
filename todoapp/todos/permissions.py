from rest_framework import permissions


class UserTodoPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(request.user)

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user
