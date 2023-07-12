from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    '''Permission to allow author-only access to the object.'''
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj.author
            or request.method in SAFE_METHODS
        )
