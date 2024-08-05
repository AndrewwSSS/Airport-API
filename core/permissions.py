from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrAuthenticatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            (
                request.user
                and request.user.is_staff
            )
            or (
                request.user.is_authenticated
                and request.method in SAFE_METHODS
            )
        )