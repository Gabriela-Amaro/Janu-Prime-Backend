from django.test import TestCase
from usuarios.serializers import AdministradorRegistrationSerializer
from usuarios.models import Administrador, Usuario
from estabelecimentos.models import Estabelecimento
from rest_framework.test import APIRequestFactory, force_authenticate


class AdministradorRegistrationSerializerTest(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

        self.superuser = Usuario.objects.create_user(
            email="superuser@example.com",
            password="password",
            is_superuser=True,
            is_staff=True,
        )

        self.usuario = Usuario.objects.create_user(
            email="usuario@example.com",
            password="password",
            is_superuser=False,
        )

        self.estabelecimento = Estabelecimento.objects.create(
            nome="Estabelecimento Teste", cnpj="12.345.678/0001-99"
        )

        self.administrador = Administrador.objects.create(
            usuario=self.usuario,
            estabelecimento=self.estabelecimento,
            nome="Administrador Teste",
            cpf="608.319.686-80",
            super_user=True,
        )

    def test_administrador_registration_serializer_valid_data(self):
        data = {
            "email": "admin@example.com",
            "password": "jprime5672",
            "password2": "jprime5672",
            "nome": "Administrador Teste",
            "cpf": "987.654.321-00",
            "estabelecimento": self.estabelecimento.id,
            "super_user": True,
        }

        request = self.factory.post("/fake-url/", data, format="json")
        request.user = self.superuser

        serializer = AdministradorRegistrationSerializer(
            data=data, context={"request": request}
        )

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["email"], data["email"])
        self.assertEqual(serializer.validated_data["nome"], data["nome"])
        self.assertEqual(serializer.validated_data["cpf"], data["cpf"])
        self.assertEqual(
            serializer.validated_data["estabelecimento"].id, data["estabelecimento"]
        )
        self.assertEqual(serializer.validated_data["super_user"], data["super_user"])

    def test_administrador_registration_serializer_invalid_data(self):
        data = {
            "email": "",
            "password": "password",
            "cpf": "608.319.686-80",
            "estabelecimento": 999999,
        }

        request = self.factory.post("/fake-url/", data, format="json")
        request.user = self.superuser

        serializer = AdministradorRegistrationSerializer(
            data=data, context={"request": request}
        )

        self.assertFalse(serializer.is_valid())

        self.assertEqual(serializer.errors["email"][0].code, "blank")
        self.assertEqual(
            serializer.errors["email"][0].title(),
            "Este Campo Não Pode Estar Em Branco.",
        )

        self.assertEqual(serializer.errors["password2"][0].code, "required")
        self.assertEqual(
            serializer.errors["password2"][0].title(), "Este Campo É Obrigatório."
        )

        self.assertEqual(serializer.errors["nome"][0].code, "required")
        self.assertEqual(
            serializer.errors["nome"][0].title(), "Este Campo É Obrigatório."
        )

        self.assertEqual(serializer.errors["cpf"][0].code, "unique")
        self.assertEqual(
            serializer.errors["cpf"][0].title(), "Administrador Com Este Cpf Já Existe."
        )

        self.assertEqual(serializer.errors["estabelecimento"][0].code, "does_not_exist")
        self.assertEqual(
            serializer.errors["estabelecimento"][0].title(),
            'Pk Inválido "999999" - Objeto Não Existe.',
        )
