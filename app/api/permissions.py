from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (obj.user_id == request.user or
                request.user.is_staff)


class IsStaff(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        print(request)
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
