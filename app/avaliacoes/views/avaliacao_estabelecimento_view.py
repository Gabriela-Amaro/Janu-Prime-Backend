from rest_framework import viewsets, permissions
from django.db.models import Q

from ..models import AvaliacaoEstabelecimento
from ..serializers import AvaliacaoEstabelecimentoSerializer
from core.permissions import IsCliente, IsPlataformAdmin
from ..permissions import IsOwnerOrReadOnly


class AvaliacaoEstabelecimentoViewSet(viewsets.ModelViewSet):
    queryset = AvaliacaoEstabelecimento.objects.all()
    serializer_class = AvaliacaoEstabelecimentoSerializer

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            return AvaliacaoEstabelecimento.objects.all()

        if user.is_authenticated and hasattr(user, "administrador"):
            estabelecimento_id = user.administrador.estabelecimento_id

            return AvaliacaoEstabelecimento.objects.filter(
                Q(estabelecimento__ativo=True)
                | Q(estabelecimento__id=estabelecimento_id)
            )

        return AvaliacaoEstabelecimento.objects.filter(estabelecimento__ativo=True)

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
