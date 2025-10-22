from rest_framework import serializers
from .models import Estabelecimento


class EstabelecimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estabelecimento
        fields = "__all__"
        read_only_fields = ["created_at", "updated_at"]
