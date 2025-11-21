from rest_framework import viewsets, permissions
from .models import FotosEspaco
from .serializers import FotosEspacoSerializer
from core.permissions import IsSuperUserOfSameEstablishmentOrPlatformAdmin


class FotosEspacoViewSet(viewsets.ModelViewSet):
    serializer_class = FotosEspacoSerializer

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            user = self.request.user

            if user.is_authenticated and user.is_superuser:
                return FotosEspaco.objects.all()

            if user.is_authenticated and user.administrador:
                return FotosEspaco.objects.filter(
                    estabelecimento=user.administrador.estabelecimento
                )

            return FotosEspaco.objects.all()
        else:
            return FotosEspaco.objects.all()

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
