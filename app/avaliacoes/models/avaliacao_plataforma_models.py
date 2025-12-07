from django.db import models
from .avaliacao_base_models import AvaliacaoBase


class AvaliacaoPlataforma(AvaliacaoBase):
    versao_app = models.CharField(
        max_length=20, blank=True, help_text="Versão do app no momento da avaliação"
    )

    class Meta(AvaliacaoBase.Meta):
        verbose_name = "Avaliação da Plataforma"
        verbose_name_plural = "Avaliações da Plataforma"

    def __str__(self):
        return f"Plataforma - {self.nota} ({self.usuario})"
