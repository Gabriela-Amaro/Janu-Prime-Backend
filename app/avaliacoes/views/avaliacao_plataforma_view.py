from rest_framework import viewsets, permissions
from ..models import AvaliacaoPlataforma
from ..serializers import AvaliacaoPlataformaSerializer
from core.permissions import IsCliente, IsPlataformAdmin
from ..permissions import IsOwnerOrReadOnly


class AvaliacaoPlataformaViewSet(viewsets.ModelViewSet):
    queryset = AvaliacaoPlataforma.objects.all()
    serializer_class = AvaliacaoPlataformaSerializer

    def get_permissions(self):
        if self.action == "create":
            return [
                permissions.IsAuthenticated(),
                (IsCliente | IsPlataformAdmin)(),
            ]  # mudar em produção, apenas clientes podem criar

        if self.action in ["update", "partial_update", "destroy"]:
            return [
                permissions.IsAuthenticated(),
                (IsOwnerOrReadOnly | IsPlataformAdmin)(),
            ]  # mudar em produção, apenas donos podem modificar

        return [permissions.AllowAny()]
