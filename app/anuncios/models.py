from django.db import models


class Anuncio(models.Model):
    estabelecimento = models.ForeignKey(
        "estabelecimentos.Estabelecimento", on_delete=models.CASCADE
    )
    imagem = models.ImageField(
        upload_to="Anuncios/", blank=True  # mudar para false em produção
    )  # configurar o upload de imagens depois
    data_expiracao = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Anuncio"
        verbose_name_plural = "Anuncios"

    def __str__(self):
        return f"Anuncio do estabelecimento {self.estabelecimento.nome}"
