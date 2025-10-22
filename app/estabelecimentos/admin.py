from django.contrib import admin
from .models import Estabelecimento

@admin.register(Estabelecimento)
class EstabelecimentoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'cnpj', 'endereco', 'telefone', 'ativo', 'created_at', 'updated_at')
    list_filter = ('ativo',)
    search_fields = ('nome', 'cnpj')
    ordering = ('created_at', 'nome')