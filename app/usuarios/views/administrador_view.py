from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Administrador
from ..serializers import (
    AdministradorRegistrationSerializer,
    AdministradorSerializer,
)
from ..permissions import (
    CanRegisterAdministrador,
    IsAdministradorOwnerOrSameEstablishmentSuperUser,
)

import logging

logger = logging.getLogger("app")


class AdministradorCadastroView(generics.CreateAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorRegistrationSerializer
    permission_classes = [CanRegisterAdministrador]

    def create(self, request, *args, **kwargs):
        reg_serializer = self.get_serializer(data=request.data)
        reg_serializer.is_valid(raise_exception=True)
        admin_instance = reg_serializer.save()

        display_serializer = AdministradorSerializer(
            admin_instance, context=self.get_serializer_context()
        )

        headers = self.get_success_headers(display_serializer.data)

        logger.info(
            "Novo administrador cadastrado: %s",
            display_serializer.data.get("email"),
            extra={
                "estabelecimento_id": display_serializer.data.get("estabelecimento")
            },
        )

        return Response(
            display_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class AdministradorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Administrador.objects.all()
    serializer_class = AdministradorSerializer
    permission_classes = [
        permissions.IsAuthenticated,
        IsAdministradorOwnerOrSameEstablishmentSuperUser,
    ]

    def perform_destroy(self, instance):
        email = instance.usuario.email
        estabelecimento_id = instance.estabelecimento.id

        instance.usuario.delete()

        logger.info(
            "Administrador deletado: %s",
            email,
            extra={"estabelecimento_id": estabelecimento_id},
        )
