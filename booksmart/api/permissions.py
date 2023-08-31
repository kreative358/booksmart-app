from rest_framework import permissions
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the records.
        return obj.owner == request.user

class IsOwner(permissions.BasePermission):
    message = "Not an owner."

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.owner

# class IsOwnerIsAdminOrReadOnly(permissions.BasePermission):
#     def has_permission(self, request, view, obj):
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         # else:
#         #     if obj.owner == request.user or request.user.is_admin:
#         #         return True

#         return obj.owner == request.user or request.user.is_admin

# class IsAdminUser(BasePermission):
#     """
#     Allows access only to admin users.
#     """

#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_staff)