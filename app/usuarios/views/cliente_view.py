from rest_framework import generics, permissions, status
from rest_framework.response import Response
from ..models import Cliente
from ..serializers import (
    ClienteRegistrationSerializer,
    ClienteSerializer,
)
from ..permissions import (
    IsClienteOwner,
)

import logging

logger = logging.getLogger("app")

class ClienteCadastroView(generics.CreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        reg_serializer = self.get_serializer(data=request.data)
        reg_serializer.is_valid(raise_exception=True)
        cliente_instance = reg_serializer.save()

        display_serializer = ClienteSerializer(
            cliente_instance, context=self.get_serializer_context()
        )

        headers = self.get_success_headers(display_serializer.data)

        logger.info(
            "Novo cliente cadastrado: %s",
            display_serializer.data.get("email")
        )

        return Response(
            display_serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [permissions.IsAuthenticated, IsClienteOwner]

    def perform_destroy(self, instance):
        email = instance.usuario.email 

        instance.usuario.delete()
        
        logger.info(
            "Cliente deletado: %s",
            email
        )