# core/permissions.py
from rest_framework.permissions import BasePermission
from .models import Usuario, Cliente, Administrador


class IsCliente(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.tipo_usuario == Usuario.TipoUsuario.CLIENTE
        )


class IsAdministrador(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.tipo_usuario == Usuario.TipoUsuario.ADMINISTRADOR
        )


class IsSuperUserAdministrador(BasePermission):
    def has_permission(self, request, view):
        is_admin = IsAdministrador().has_permission(request, view)
        return (
            is_admin
            and hasattr(request.user, "administrador")
            and request.user.administrador.super_user
        )


class CanRegisterAdministrador(BasePermission):
    message = "Você não tem permissão para cadastrar novos funcionários."

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.user.is_superuser:
            return True

        if request.user.tipo_usuario == Usuario.TipoUsuario.ADMINISTRADOR:
            # hasattr previne erro caso o perfil ainda não exista por algum motivo
            if (
                hasattr(request.user, "administrador")
                and request.user.administrador.super_user
            ):
                return True

        return False


class IsClienteOwner(BasePermission):
    message = "Você não tem permissão para acessar os dados deste cliente."

    def has_object_permission(self, request, view, obj):
        is_cliente_and_owner = (
            IsCliente().has_permission(request, view) and obj.usuario == request.user
        )

        return is_cliente_and_owner or request.user.is_superuser


class IsAdministradorOwnerOrSameEstablishmentSuperUser(BasePermission):
    message = "Você não tem permissão para acessar os dados deste funcionário."

    def has_object_permission(self, request, view, obj):
        is_admin_and_owner = (
            IsAdministrador().has_permission(request, view)
            and obj.usuario == request.user
        )

        is_platform_superuser = request.user.is_superuser

        is_same_establishment_superuser = False

        if (
            hasattr(request.user, "administrador")
            and request.user.administrador.super_user
        ):
            if request.user.administrador.estabelecimento == obj.estabelecimento:
                is_same_establishment_superuser = True

        return (
            is_admin_and_owner
            or is_platform_superuser
            or is_same_establishment_superuser
        )
