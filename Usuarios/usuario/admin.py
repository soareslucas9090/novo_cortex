"""
Admin para o app Usuarios
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Usuario, Contato, Endereco, CodigoRedefinicaoSenha


class ContatoInline(admin.TabularInline):
    model = Contato
    extra = 0
    fields = ('email', 'telefone')
    can_delete = True


class EnderecoInline(admin.TabularInline):
    model = Endereco
    extra = 0
    fields = ('logradouro', 'num_casa', 'bairro', 'cidade', 'estado', 'cep')
    can_delete = True


@admin.register(Usuario)
class UsuarioAdmin(BaseUserAdmin):
    list_display = (
        'cpf',
        'nome',
        'ativo',
        'is_staff',
        'is_admin',
        'campus',
    )
    
    list_filter = (
        'ativo',
        'is_staff',
        'is_superuser',
        'is_admin',
        'campus',
    )
    
    search_fields = (
        'cpf',
        'nome',
    )
    
    fieldsets = (
        (None, {
            'fields': ('cpf', 'password')
        }),
        ('Informações Pessoais', {
            'fields': (
                'nome',
                'data_nascimento',
                'campus',
            )
        }),
        ('Permissões', {
            'fields': (
                'ativo',
                'is_staff',
                'is_superuser',
                'is_admin',
            )
        }),
        ('Datas', {
            'fields': (
                'data_ingresso',
                'last_login',
            )
        }),
    )
    
    ordering = ['nome']
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'cpf',
                'nome',
                'data_nascimento',
                'campus',
                'password1',
                'password2',
            ),
        }),
    )
    
    inlines = [ContatoInline, EnderecoInline]


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'email',
        'telefone',
        'created_at',
    )
    
    list_filter = (
        'created_at',
    )
    
    search_fields = (
        'usuario__nome',
        'usuario__cpf',
        'email',
        'telefone',
    )


@admin.register(Endereco)
class EnderecoAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'logradouro',
        'num_casa',
        'cidade',
        'estado',
    )
    
    list_filter = (
        'estado',
        'cidade',
    )
    
    search_fields = (
        'usuario__nome',
        'usuario__cpf',
        'logradouro',
        'cidade',
    )


@admin.register(CodigoRedefinicaoSenha)
class CodigoRedefinicaoSenhaAdmin(admin.ModelAdmin):
    list_display = (
        'usuario',
        'codigo',
        'validado',
        'tempo_expiracao',
        'created_at',
    )
    
    list_filter = (
        'validado',
        'created_at',
    )
    
    search_fields = (
        'usuario__nome',
        'usuario__cpf',
    )
