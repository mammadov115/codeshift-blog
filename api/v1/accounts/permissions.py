from rest_framework import permissions


class IsAnonymousUser(permissions.BasePermission):
    """
    Custom permission to allow only anonymous users to access a specific endpoint.
    Prevents authenticated users from performing actions like registration again.
    """

    message = "You are already authenticated. Registration is only available for anonymous users."

    def has_permission(self, request, view):
        """
        Grant access only if the user is not authenticated.
        """
        return not request.user or not request.user.is_authenticated


class IsAuthorUser(permissions.BasePermission):
    """
    Permission to allow access only to authors for their own profile.
    """

    message = "You must be the author to access or edit this profile."

    def has_object_permission(self, request, view, obj):
        # Allow read-only access to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write access only to the owner (author)
        return obj.user == request.user
    

class IsReaderUser(permissions.BasePermission):
    """
    Permission to allow access only to the reader for their own profile.
    """

    message = "You must be the reader to access or edit this profile."

    def has_object_permission(self, request, view, obj):
        # Allow read-only access to anyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write access only to the owner (reader)
        return obj.user == request.user