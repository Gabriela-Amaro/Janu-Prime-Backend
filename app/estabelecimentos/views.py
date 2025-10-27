from rest_framework import viewsets, permissions
from .models import Estabelecimento
from .serializers import EstabelecimentoSerializer
from .permissions import IsSuperUserOfSameEstablishmentOrPlatformAdmin


class EstabelecimentoViewSet(viewsets.ModelViewSet):
    serializer_class = EstabelecimentoSerializer

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            user = self.request.user

            if user.is_authenticated and user.is_superuser:
                return Estabelecimento.objects.all()

            if user.is_authenticated and user.administrador:
                return Estabelecimento.objects.filter(
                    id=user.administrador.estabelecimento.id
                )

            return Estabelecimento.objects.filter(ativo=True)
        else:
            return Estabelecimento.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSuperUserOfSameEstablishmentOrPlatformAdmin]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        pass

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request, "view": self})
        return context