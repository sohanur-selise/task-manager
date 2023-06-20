from rest_framework.permissions import BasePermission


class CanCreateTaskPermission(BasePermission):
    message = 'You do not have permission to create tasks.'

    def has_permission(self, request, view):
        # Check if the user has the "admin" or "manager" role
        user = request.user
        return user.role in ['admin', 'manager']