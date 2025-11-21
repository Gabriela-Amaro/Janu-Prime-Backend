from rest_framework import serializers
from .models import Produto
from core.permissions import IsEstablishmentAdmin, IsPlataformAdmin


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = "__all__"
        read_only_fields = [
            "id",
            "estabelecimento",
            "pontos",
            "created_at",
            "updated_at",
        ]

    def get_fields(self):
        """
        Modifica os campos dinamicamente com base no usuário e na ação.
        """
        fields = super().get_fields()

        request = self.context.get("request")
        view = self.context.get("view")

        if not request or not view:
            return fields

        is_superuser = IsPlataformAdmin().has_permission(request, view)
        is_admin = IsEstablishmentAdmin().has_permission(request, view)

        is_privileged = is_superuser or is_admin

        if view.action in ["list", "retrieve"] and not is_privileged:
            fields.pop("created_at", None)
            fields.pop("updated_at", None)
            fields.pop("ativo", None)
            fields.pop("preco", None)

        return fields

    def create(self, validated_data):
        requesting_user = self.context["request"].user

        if not requesting_user.is_superuser and not hasattr(
            requesting_user, "administrador"
        ):
            raise serializers.ValidationError(
                "Usuário não possui permissão para criar um produto."
            )

        if not requesting_user.is_superuser:
            validated_data["estabelecimento"] = (
                requesting_user.administrador.estabelecimento
            )

        try:
            produto = Produto.objects.create(**validated_data)

        except Exception as e:
            raise serializers.ValidationError(
                f"Ocorreu um erro durante o registro: {e}"
            )

        return produto
