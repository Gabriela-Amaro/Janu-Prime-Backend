from rest_framework import viewsets, permissions
from .models import Produto
from .serializers import ProdutoSerializer
from .permissions import IsSuperUserOfSameEstablishmentOrPlatformAdmin


class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            user = self.request.user

            if user.is_authenticated and user.is_superuser:
                return Produto.objects.all()

            if user.is_authenticated and user.administrador:
                return Produto.objects.filter(
                    estabelecimento=user.administrador.estabelecimento
                )

            return Produto.objects.filter(ativo=True)
        else:
            return Produto.objects.all()

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSuperUserOfSameEstablishmentOrPlatformAdmin]

        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"request": self.request, "view": self})
        return context