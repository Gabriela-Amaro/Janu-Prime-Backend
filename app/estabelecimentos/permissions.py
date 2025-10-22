from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperUserOfSameEstablishmentOrPlatformAdmin(BasePermission):
    message = "Você não tem permissão para editar ou excluir este estabelecimento."

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True

        if request.method not in SAFE_METHODS:
            return (
                hasattr(request.user, 'administrador') and
                request.user.administrador.super_user and
                request.user.administrador.estabelecimento == obj
            )
        
        return True