from django.db import models


class FotosEspaco(models.Model):
    estabelecimento = models.ForeignKey(
        "estabelecimentos.Estabelecimento", on_delete=models.CASCADE
    )
    foto = models.ImageField(
        upload_to="Fotos_Espaco/", blank=True  # mudar para false em produção
    )  # configurar o upload de imagens depois
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Foto do Espaço"
        verbose_name_plural = "Fotos do Espaço"

    def __str__(self):
        return f"Foto do espaço do estabelecimento {self.estabelecimento.nome}"
