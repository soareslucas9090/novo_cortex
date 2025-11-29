"""
Admin para o app Usuarios
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Perfil


class PerfilInline(admin.TabularInline):
    model = Perfil
    extra = 0
    fields = ('tipo', 'bio', 'avatar', 'status')
    can_delete = True


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = (
        'email',
        'nome',
        'is_active',
        'is_staff',
        'email_verificado',
        'status',
        'date_joined'
    )
    
    list_filter = (
        'is_active',
        'is_staff',
        'is_superuser',
        'email_verificado',
        'status',
        'date_joined'
    )
    
    search_fields = (
        'email',
        'nome'
    )
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'telefone',
                'data_nascimento',
                'email_verificado',
                'status'
            )
        }),
    )
    
    ordering = ['email']
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Informações Adicionais', {
            'fields': (
                'email',
                'telefone',
                'data_nascimento',
                'email_verificado',
                'status'
            )
        }),
    )
    
    inlines = [PerfilInline]


@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'tipo',
        'status',
        'created_at'
    )
    
    list_filter = (
        'tipo',
        'status',
        'created_at'
    )
    
    search_fields = (
        'usuario__email',
        'nome'
    )
    
    fieldsets = (
        ('Informações Principais', {
            'fields': (
                'usuario',
                'tipo',
                'status'
            )
        }),
        ('Informações Adicionais', {
            'fields': (
                'bio',
                'avatar'
            )
        }),
    )
