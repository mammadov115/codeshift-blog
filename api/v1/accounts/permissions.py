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
