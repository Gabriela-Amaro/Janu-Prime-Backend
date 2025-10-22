from django.db import models

from localflavor.br.models import BRCNPJField
from phonenumber_field.modelfields import PhoneNumberField


class Estabelecimento(models.Model):
    nome = models.CharField(max_length=255)
    endereco = models.CharField(max_length=255, blank=True)
    telefone = PhoneNumberField(region="BR", blank=True)
    descricao = models.TextField(blank=True)
    logotipo = models.ImageField(
        upload_to="logotipos/", blank=True
    )  # configurar o upload de imagens depois
    cnpj = BRCNPJField(unique=True, help_text="Formato: 12.345.678/0001-99")
    horario_funcionamento = models.JSONField(
        default=dict, blank=True
    )  # Exemplo: {"segunda": "08:00-18:00", "terça": "08:00-18:00", ...}
    ativo = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Estabelecimento"
        verbose_name_plural = "Estabelecimentos"
