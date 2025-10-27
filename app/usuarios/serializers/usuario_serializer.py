from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from ..models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["email", "tipo_usuario", 'created_at', 'updated_at']
        read_only_fields = ["tipo_usuario", 'created_at', 'updated_at']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        required=True, write_only=True, label="Senha Antiga"
    )
    new_password = serializers.CharField(
        required=True, write_only=True, label="Nova Senha"
    )
    new_password2 = serializers.CharField(
        required=True, write_only=True, label="Confirme a Nova Senha"
    )

    def validate_old_password(self, value):
        user = self.context["request"].user
        if not user.check_password(value):
            raise serializers.ValidationError("A senha antiga está incorreta.")
        return value

    def validate(self, data):
        if data["new_password"] != data["new_password2"]:
            raise serializers.ValidationError(
                {"new_password": "As novas senhas não coincidem."}
            )

        try:
            validate_password(data["new_password"], self.context["request"].user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"new_password": list(e.messages)})

        return data

    def save(self, **kwargs):
        user = self.context["request"].user
        user.set_password(self.validated_data["new_password"])
        user.save()
        return user
