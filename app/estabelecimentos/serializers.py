from rest_framework import serializers
from .models import Estabelecimento


class EstabelecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estabelecimento
        fields = "__all__"
        read_only_fields = ["id", "cnpj", "created_at", "updated_at"]

    def get_fields(self):
        """
        Modifica os campos dinamicamente com base no usuário e na ação.
        """
        fields = super().get_fields()

        request = self.context.get("request")
        view = self.context.get("view")

        if not request or not view:
            return fields

        user = request.user
        is_superuser = user.is_authenticated and user.is_superuser
        is_admin = user.is_authenticated and hasattr(user, 'administrador') and user.administrador
        
        is_privileged = is_superuser or is_admin

        if view.action in ["list", "retrieve"] and not is_privileged:
            fields.pop("created_at", None)
            fields.pop("updated_at", None)
            fields.pop("ativo", None)

        return fields