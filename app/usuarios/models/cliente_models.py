from django.db import models
from localflavor.br.models import BRCPFField
from phonenumber_field.modelfields import PhoneNumberField
from usuarios.models.usuario_models import Usuario


class Cliente(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    nome = models.CharField(max_length=255)
    cpf = BRCPFField(unique=True)
    telefone = PhoneNumberField(region="BR", unique=True)
    pontos = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome
