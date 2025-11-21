from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FotosEspaco


@admin.register(FotosEspaco)
class FotosEspacoAdmin(admin.ModelAdmin):
    list_display = ("id", "estabelecimento", "foto", "created_at")
    list_filter = ("estabelecimento",)
    search_fields = ("estabelecimento__nome",)
