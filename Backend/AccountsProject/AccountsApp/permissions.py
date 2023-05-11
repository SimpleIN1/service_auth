from rest_framework.permissions import BasePermission


class IsVerifyEmailAndActive(BasePermission):

    def has_permission(self, request, view):
        if bool(request.user.is_verify) or bool(request.user.is_active):
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        return False


class IsDirector(BasePermission):
    def has_permission(self, request, view):
        if request.user.type_user == 1:
            return True
        return False