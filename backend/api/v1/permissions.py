from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthor(BasePermission):
    """Permission to allow author-only access to the object."""
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or request.method in SAFE_METHODS)
