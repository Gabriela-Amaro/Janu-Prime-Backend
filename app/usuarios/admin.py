from django.contrib import admin
from .models import Usuario, Administrador, Cliente


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "tipo_usuario",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "created_at",
        "updated_at",
    )
    list_filter = ("tipo_usuario", "is_active", "is_staff", "is_superuser")
    search_fields = ("email", "id")
    ordering = ("created_at", "email")


@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = (
        "usuario__id",
        "usuario__email",
        "estabelecimento__nome",
        "nome",
        "cpf",
        "super_user",
        "usuario__created_at",
        "usuario__updated_at",
    )
    list_filter = ("super_user",)
    search_fields = ("nome", "cpf", "usuario__id", "usuario__email")
    ordering = ("usuario__created_at", "nome")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "usuario__id",
        "usuario__email",
        "nome",
        "cpf",
        "telefone",
        "pontos",
        "usuario__created_at",
        "usuario__updated_at",
    )
    search_fields = ("usuario__email", "nome", "cpf", "usuario__id")
    ordering = ("usuario__created_at", "nome", "pontos")
