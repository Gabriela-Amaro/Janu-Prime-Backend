from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.forms import widgets
from .models import Anuncio

@admin.register(Anuncio)
class AnuncioAdmin(admin.ModelAdmin):
    list_display = ('id', 'estabelecimento', 'imagem', 'data_expiracao', 'created_at')
    list_filter = ('estabelecimento',)
    search_fields = ('estabelecimento__nome',)