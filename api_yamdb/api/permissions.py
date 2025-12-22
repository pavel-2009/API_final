from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.role == 'admin'
                 or request.user.is_superuser)
        )


class IsNotUser(BasePermission):
    def has_permission(self, request, view):
        return not (
            request.user.is_authenticated
            and request.user.role == 'user'
        )


class IsNotModerator(BasePermission):
    def has_permission(self, request, view):
        return not (
            request.user.is_authenticated
            and request.user.role == 'moderator'
        )


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True

        return (
            request.user.is_authenticated
            and (obj.author == request.user
                 or request.user.role == 'admin'
                 or request.user.is_superuser
                 or request.user.role == 'moderator')
        )
