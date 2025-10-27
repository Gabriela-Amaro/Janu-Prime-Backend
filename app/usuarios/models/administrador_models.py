from django.db import models
from localflavor.br.models import BRCPFField
from usuarios.models.usuario_models import Usuario

class Administrador(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True)
    estabelecimento = models.ForeignKey(
        "estabelecimentos.Estabelecimento", on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=255)
    cpf = BRCPFField(unique=True)
    super_user = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Administrador"
        verbose_name_plural = "Administradores"

    def __str__(self):
        return self.nome
