from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Разрешено просматривать для всех
        if request.method in permissions.SAFE_METHODS:
            return True

        # Разрешено редактировать только владельцу
        return obj.owner == request.user
