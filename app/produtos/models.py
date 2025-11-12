from django.db import models


class Produto(models.Model):
    estabelecimento = models.ForeignKey(
        "estabelecimentos.Estabelecimento", on_delete=models.CASCADE
    )
    nome = models.CharField(max_length=255)
    descricao = models.TextField(blank=True)
    imagem = models.ImageField(
        upload_to="produtos/", blank=True
    )  # configurar o upload de imagens depois
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    pontos = models.IntegerField(default=0, blank=True)
    ativo = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
