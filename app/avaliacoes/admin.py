from django.contrib import admin

from .models import AvaliacaoEstabelecimento, AvaliacaoPlataforma


@admin.register(AvaliacaoEstabelecimento)
class AvaliacaoEstabelecimentoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario__email",
        "estabelecimento",
        "nota",
        "comentario",
        "created_at",
        "updated_at",
    )
    list_filter = ("estabelecimento", "nota")
    search_fields = ("usuario__email", "estabelecimento__nome", "comentario")
    ordering = ("-created_at", "nota")


@admin.register(AvaliacaoPlataforma)
class AvaliacaoPlataformaAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "usuario__email",
        "versao_app",
        "nota",
        "comentario",
        "created_at",
        "updated_at",
    )
    list_filter = ("versao_app", "nota")
    search_fields = ("usuario__email", "versao_app", "comentario")
    ordering = ("-created_at", "nota")
