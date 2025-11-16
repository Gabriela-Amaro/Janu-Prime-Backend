from django.utils import timezone
from rest_framework import viewsets, permissions
from .models import Anuncio
from .serializers import AnuncioSerializer
from core.permissions import IsSuperUserOfSameEstablishmentOrPlatformAdmin


class AnuncioViewSet(viewsets.ModelViewSet):
    serializer_class = AnuncioSerializer

    def get_queryset(self):
        if self.action in ["list", "retrieve"]:
            user = self.request.user

            if user.is_authenticated and user.is_superuser:
                return Anuncio.objects.all()

            if user.is_authenticated and user.administrador:
                return Anuncio.objects.filter(
                    estabelecimento=user.administrador.estabelecimento
                )

            return Anuncio.objects.filter(data_expiracao__gt=timezone.now())
        else:
            return Anuncio.objects.all()

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
