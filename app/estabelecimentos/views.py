from rest_framework import viewsets, permissions
from .models import Estabelecimento
from .serializers import EstabelecimentoSerializer
from .permissions import IsSuperUserOfSameEstablishmentOrPlatformAdmin

class EstabelecimentoViewSet(viewsets.ModelViewSet):
    queryset = Estabelecimento.objects.all()
    serializer_class = EstabelecimentoSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [IsSuperUserOfSameEstablishmentOrPlatformAdmin]

        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        pass