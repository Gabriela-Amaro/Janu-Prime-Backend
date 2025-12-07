from rest_framework import serializers


class AvaliacaoBaseSerializer(serializers.ModelSerializer):
    nome_autor = serializers.SerializerMethodField()

    class Meta:
        fields = ["id", "usuario", "nome_autor", "nota", "comentario", "created_at"]
        read_only_fields = ["id", "created_at", "nome_autor", "usuario"]

    def get_nome_autor(self, obj):
        usuario = obj.usuario

        if hasattr(usuario, "cliente"):
            return usuario.cliente.nome

        if hasattr(usuario, "administrador"):
            return f"{usuario.administrador.nome} (Adm)"

        return usuario.email

    def create(self, validated_data):
        validated_data["usuario"] = self.context["request"].user
        return super().create(validated_data)
