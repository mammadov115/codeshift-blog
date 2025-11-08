from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only admins to edit categories.
    Read-only for everyone else.
    """

    def has_permission(self, request, view):
        # SAFE_METHODS: GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the post's author to edit or delete it.
    Read-only access is granted to all other users.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS include GET, HEAD, and OPTIONS — always allowed.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only allow the author of the post to edit/delete.
        return hasattr(request.user, "authorprofile") and obj.author.user == request.user


class IsVerifiedAuthor(permissions.BasePermission):
    """
    Custom permission that allows only verified authors to create new posts.
    """

    def has_permission(self, request, view):
        # Read-only requests are always allowed.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Ensure the user has an author profile and is verified.
        author_profile = getattr(request.user, "authorprofile", None)
        return author_profile is not None and author_profile.verified
