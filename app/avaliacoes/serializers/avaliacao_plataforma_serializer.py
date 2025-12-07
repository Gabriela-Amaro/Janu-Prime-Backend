from ..models import AvaliacaoPlataforma
from .avaliacao_base_serializer import AvaliacaoBaseSerializer
from rest_framework import serializers


class AvaliacaoPlataformaSerializer(AvaliacaoBaseSerializer):
    class Meta(AvaliacaoBaseSerializer.Meta):
        model = AvaliacaoPlataforma
        fields = AvaliacaoBaseSerializer.Meta.fields + ["versao_app"]
        read_only_fields = AvaliacaoBaseSerializer.Meta.read_only_fields + [
            "versao_app"
        ]

    def validate(self, data):
        user = self.context["request"].user

        if self.instance is None:
            if AvaliacaoPlataforma.objects.filter(usuario=user).exists():
                raise serializers.ValidationError("Você já fez uma avaliação.")

        return data
