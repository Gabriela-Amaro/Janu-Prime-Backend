from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class AvaliacaoBase(models.Model):
    """
    Classe abstrata que contém a lógica comum para qualquer avaliação.
    Não cria tabela no banco de dados.
    """

    usuario = models.ForeignKey(
        "usuarios.Usuario",
        on_delete=models.SET_NULL,
        null=True,
        related_name="%(class)s_autor",
    )
    nota = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nota de 1 a 5",
    )
    comentario = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ["-created_at"]
