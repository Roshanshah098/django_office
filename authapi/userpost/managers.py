# managers.py
from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    """
    Allows access only to authors (for creating and updating posts).
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "author_profile")
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "author_profile")
        )


class IsReader(BasePermission):
    """
    Allows access only to readers (for reading posts).
    """

    def has_permission(self, request, view):
        # Allow list view for any authenticated user
        if view.action == "list":
            return request.user and request.user.is_authenticated
        # Other actions require the user to have a reader_profile
        return (
            request.user
            and request.user.is_authenticated
            and hasattr(request.user, "reader_profile")
        )
