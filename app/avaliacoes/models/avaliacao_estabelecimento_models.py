from django.db import models
from .avaliacao_base_models import AvaliacaoBase


class AvaliacaoEstabelecimento(AvaliacaoBase):
    estabelecimento = models.ForeignKey(
        "estabelecimentos.Estabelecimento",
        on_delete=models.CASCADE,
        related_name="avaliacoes",
    )

    class Meta(AvaliacaoBase.Meta):
        verbose_name = "Avaliação de Estabelecimento"
        verbose_name_plural = "Avaliações de Estabelecimentos"

    def __str__(self):
        return f"{self.estabelecimento.nome} - {self.nota} ({self.usuario})"
