from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'admin'
                                                or request.user.is_superuser)

class IsNotUserAndModeratorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        return (request.user.is_authenticated and request.user.role != 'user' and
            request.user.role != 'moderator')