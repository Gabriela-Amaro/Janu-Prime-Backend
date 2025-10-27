from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from ..models import Usuario, Administrador
from estabelecimentos.models import Estabelecimento
from ..serializers import UsuarioSerializer


class AdministradorSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)
    estabelecimento = serializers.StringRelatedField()

    class Meta:
        model = Administrador
        fields = [
            "usuario",
            "nome",
            "cpf",
            "estabelecimento",
            "super_user",
        ]
        read_only_fields = [
            "cpf",
            "estabelecimento",
            "super_user",
        ]


class AdministradorRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True, required=True, label="Senha", style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirme a senha",
        style={"input_type": "password"},
    )
    estabelecimento = serializers.PrimaryKeyRelatedField(
        queryset=Estabelecimento.objects.all()
    )

    class Meta:
        model = Administrador
        fields = [
            "email",
            "password",
            "password2",
            "nome",
            "cpf",
            "estabelecimento",
            "super_user",
        ]
        read_only_fields = ["is_staff"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        requesting_user = self.context["request"].user

        if not requesting_user.is_superuser:
            self.fields["estabelecimento"].read_only = True
            self.fields["super_user"].read_only = True

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})

        try:
            validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        requesting_user = self.context["request"].user

        is_creating_superuser = attrs.get("super_user", False)

        if is_creating_superuser and not requesting_user.is_superuser:
            raise serializers.ValidationError(
                "Você não tem permissão para criar um funcionário super-usuário."
            )

        return attrs

    def create(self, validated_data):
        requesting_user = self.context["request"].user

        if not requesting_user.is_superuser:
            try:
                validated_data["estabelecimento"] = (
                    requesting_user.administrador.estabelecimento
                )
            except Administrador.DoesNotExist:
                raise serializers.ValidationError(
                    "O seu usuário administrador não está associado a um estabelecimento."
                )
            validated_data["super_user"] = False

        email = validated_data.pop("email")
        password = validated_data.pop("password")
        validated_data.pop("password2")

        try:
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    email=email,
                    password=password,
                    tipo_usuario=Usuario.TipoUsuario.ADMINISTRADOR,
                )
                administrador = Administrador.objects.create(
                    usuario=usuario, **validated_data
                )
        except Exception as e:
            raise serializers.ValidationError(
                f"Ocorreu um erro durante o registro: {e}"
            )

        return administrador
