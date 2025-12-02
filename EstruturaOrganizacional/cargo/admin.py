from django.contrib import admin

from EstruturaOrganizacional.cargo.models import Cargo


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Cargo.
    """
    list_display = ('id', 'descricao', 'created_at', 'updated_at')
    list_display_links = ('id', 'descricao')
    search_fields = ('descricao',)
    ordering = ('descricao',)
    readonly_fields = ('created_at', 'updated_at')
