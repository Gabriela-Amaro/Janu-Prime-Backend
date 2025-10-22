from django.test import TestCase
from usuarios.serializers import ClienteRegistrationSerializer
from usuarios.models import Cliente, Usuario


class ClienteRegistrationSerializerTest(TestCase):

    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            email="user@example.com", password="@Password123"
        )

        self.existing_cliente = Cliente.objects.create(
            usuario_id=self.usuario.id,
            nome="Existing User",
            cpf="915.377.136-20",
            telefone="+553436751022",
        )

    def test_cliente_registration_serializer_valid_data(self):
        data = {
            "email": "test@example.com",
            "password": "@Password123",
            "password2": "@Password123",
            "nome": "Test User",
            "cpf": "085.981.021-64",
            "telefone": "+553837515855",
        }

        serializer = ClienteRegistrationSerializer(data=data)

        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["email"], data["email"])
        self.assertEqual(serializer.validated_data["nome"], data["nome"])
        self.assertEqual(serializer.validated_data["cpf"], data["cpf"])
        self.assertEqual(serializer.validated_data["telefone"], data["telefone"])

    def test_cliente_registration_serializer_invalid_data(self):
        data = {
            "email": "",
            "password": "@Password123",
            "cpf": "915.377.136-20",
            "telefone": "+553436751022",
        }

        serializer = ClienteRegistrationSerializer(data=data)

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
            serializer.errors["cpf"][0].title(), "Cliente Com Este Cpf Já Existe."
        )

        self.assertEqual(serializer.errors["telefone"][0].code, "unique")
        self.assertEqual(
            serializer.errors["telefone"][0].title(),
            "Cliente Com Este Telefone Já Existe.",
        )
