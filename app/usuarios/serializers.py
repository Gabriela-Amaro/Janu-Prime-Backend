from rest_framework import serializers
from django.db import transaction
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Usuario, Cliente, Administrador
from estabelecimentos.models import Estabelecimento


class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ["email", "tipo_usuario"]


class ClienteSerializer(serializers.ModelSerializer):
    usuario = UsuarioSerializer(read_only=True)

    class Meta:
        model = Cliente
        fields = [
            "usuario",
            "nome",
            "cpf",
            "telefone",
            "pontos",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["cpf", "pontos", "created_at", "updated_at"]


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
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "cpf",
            "estabelecimento",
            "super_user",
            "created_at",
            "updated_at",
        ]


class ClienteRegistrationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        write_only=True, required=True, label="Senha", style={"input_type": "password"}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        label="Confirme a senha",
        style={"input_type": "password"},
    )

    class Meta:
        model = Cliente
        fields = ["email", "password", "password2", "nome", "cpf", "telefone"]
        read_only_fields = ["created_at", "updated_at", "is_staff"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "As senhas não coincidem."})

        try:
            validate_password(attrs["password"])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})

        return attrs

    def create(self, validated_data):
        email = validated_data.pop("email")
        password = validated_data.pop("password")
        validated_data.pop("password2")

        try:
            with transaction.atomic():
                usuario = Usuario.objects.create_user(
                    email=email,
                    password=password,
                    tipo_usuario=Usuario.TipoUsuario.CLIENTE,
                )
                cliente = Cliente.objects.create(usuario=usuario, **validated_data)
        except Exception as e:
            raise serializers.ValidationError(
                f"Ocorreu um erro durante o registro: {e}"
            )

        return cliente


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
        read_only_fields = ["created_at", "updated_at", "is_staff"]

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
