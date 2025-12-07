from ..models import AvaliacaoEstabelecimento
from .avaliacao_base_serializer import AvaliacaoBaseSerializer
from rest_framework import serializers


class AvaliacaoEstabelecimentoSerializer(AvaliacaoBaseSerializer):
    class Meta(AvaliacaoBaseSerializer.Meta):
        model = AvaliacaoEstabelecimento
        fields = AvaliacaoBaseSerializer.Meta.fields + ["estabelecimento"]
        read_only_fields = AvaliacaoBaseSerializer.Meta.read_only_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance is not None:
            self.fields["estabelecimento"].read_only = True

    def validate(self, data):
        if self.instance is None:
            estabelecimento = data.get("estabelecimento")
            user = self.context["request"].user

            if estabelecimento and not estabelecimento.ativo:
                raise serializers.ValidationError(
                    {
                        "estabelecimento": "Este estabelecimento está inativo e não pode receber avaliações."
                    }
                )

            if AvaliacaoEstabelecimento.objects.filter(
                usuario=user, estabelecimento=estabelecimento
            ).exists():
                raise serializers.ValidationError(
                    "Você já avaliou este estabelecimento."
                )

        return data
