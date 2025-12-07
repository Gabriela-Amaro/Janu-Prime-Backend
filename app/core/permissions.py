from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsPlataformAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True

        return False


class IsEstablishmentAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "administrador")

    def has_object_permission(self, request, view, obj):
        return (
            self.has_permission(request, view)
            and request.user.administrador.estabelecimento == obj.estabelecimento
        )


class IsEstablishmentSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, "administrador")
            and request.user.administrador.super_user
        )

    def has_object_permission(self, request, view, obj):
        return (
            self.has_permission(request, view)
            and request.user.administrador.estabelecimento == obj.estabelecimento
        )


class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and hasattr(request.user, "cliente")

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and request.user == obj.usuario


class IsSuperUserOfSameEstablishmentOrPlatformAdmin(BasePermission):
    message = "Você não tem permissão."

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method not in SAFE_METHODS:
            return (
                hasattr(request.user, "administrador")
                and request.user.administrador.super_user
                and request.user.administrador.estabelecimento == obj.estabelecimento
            )

        return True
