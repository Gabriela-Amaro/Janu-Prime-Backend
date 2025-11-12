from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "nome",
        "estabelecimento",
        "descricao",
        "imagem",
        "preco",
        "pontos",
        "ativo",
        "created_at",
        "updated_at",
    )
    list_filter = ("estabelecimento", "ativo")
    search_fields = ("nome", "estabelecimento__nome")
    ordering = ("created_at", "nome", "estabelecimento__nome", "preco")
