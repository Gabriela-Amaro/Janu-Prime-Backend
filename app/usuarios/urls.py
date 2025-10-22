from django.urls import path
from .views import (
    ChangePasswordView,
    ClienteCadastroView,
    AdministradorCadastroView,
    ClienteDetailView,
    AdministradorDetailView,
)

urlpatterns = [
    # Clientes
    path("clientes/cadastro/", ClienteCadastroView.as_view(), name="cliente-cadastro"),
    path(
        "clientes/<int:pk>/", ClienteDetailView.as_view(), name="cliente-detail"
    ),  # Read/Update/Delete
    # Administradores
    path(
        "administradores/cadastro/",
        AdministradorCadastroView.as_view(),
        name="administrador-cadastro",
    ),
    path(
        "administradores/<int:pk>/",
        AdministradorDetailView.as_view(),
        name="administrador-detail",
    ),  # Read/Update/Delete
    # Usuario geral
    path(
        "usuarios/change-password/",
        ChangePasswordView.as_view(),
        name="change-password",
    ),
]
