from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin
from AppCore.core.business.business_mixin import ModelBusinessMixin

from .business import UsuarioBusiness
from .helpers import UsuarioHelper
from . import choices


class GerenciadorUsuario(Base404ExceptionManager):
    def criar_usuario(self, email, nome, senha=None, telefone=None, data_nascimento=None, perfis=None, **campos_extras):
        if not email:
            raise ValueError('O usuário deve ter um email')
        if not nome:
            raise ValueError('O usuário deve ter um nome')
        
        email = self.normalize_email(email)
        
        campos_extras.setdefault('is_staff', False)
        campos_extras.setdefault('is_superuser', False)
        campos_extras.setdefault('is_active', True)
        campos_extras.setdefault('status', choices.USUARIO_STATUS_ATIVO)
        
        usuario = self.model(
            email=email,
            nome=nome,
            telefone=telefone,
            data_nascimento=data_nascimento,
            **campos_extras
        )
        
        if senha:
            usuario.set_password(senha)
        
        usuario.save()
        
        return usuario
    
    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('status', choices.USUARIO_STATUS_ATIVO)
        extra_fields.setdefault('email_verificado', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superusuário deve ter is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superusuário deve ter is_superuser=True')
        
        return self.criar_usuario(
            email=email,
            nome=name,
            senha=password,
            **extra_fields
        )
    

class Usuario(
    ModelHelperMixin, ModelBusinessMixin, AbstractBaseUser, PermissionsMixin, BasicModel
):
    nome = models.CharField(
        'Nome',
        max_length=150,
    )
    email = models.EmailField('Email', unique=True)
    email_verificado = models.BooleanField(
        'Email Verificado',
        default=False
    )
    telefone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True,
        null=True
    )
    data_nascimento = models.DateField(
        'Data de Nascimento',
        blank=True,
        null=True
    )
    status = models.IntegerField(
        'Status',
        choices=choices.USUARIO_STATUS_OPCOES,
        default=choices.USUARIO_STATUS_ATIVO
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True
    )
    is_staff = models.BooleanField(
        'Equipe',
        default=False
    )
    is_superuser = models.BooleanField(
        'Superusuário',
        default=False
    )
    date_joined = models.DateTimeField(
        'Data de Criação',
        default=timezone.now
    )

    objects = GerenciadorUsuario()
    USERNAME_FIELD = "email"
    
    helper_class = UsuarioHelper
    business_class = UsuarioBusiness
    
    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['-date_joined']

    def __str__(self):
        return self.nome

    @property
    def conta_business(self):
        from Usuarios.conta.business import ContaBusiness

        return ContaBusiness(object_instance=self)

    @property
    def conta_helper(self):
        from Usuarios.conta.helpers import ContaHelper

        return ContaHelper(object_instance=self)


class CodigoRedefinicaoSenha(BasicModel):
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='codigo_redefinicao_senha',
        verbose_name='Usuário'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    tempo_expiracao = models.DateTimeField(null=False)
    codigo = models.IntegerField(null=False)
    validado = models.BooleanField(default=False)

    def __str__(self):
        return f"Usuario {self.usuario}, codigo {self.codigo}"

    class Meta:
        db_table = 'password_reset_codes'
        verbose_name = 'Código de redefinição de senha'
        verbose_name_plural = 'Códigos de redefinição de senha'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "codigo"], name="unique_code_user_constraint"
            )
        ]


class Perfil(BasicModel, ModelHelperMixin):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='perfis',
        verbose_name='Usuário'
    )
    tipo = models.CharField(
        'Tipo',
        max_length=10,
        choices=choices.PERFIL_TIPO_OPCOES,
        default=choices.PERFIL_TIPO_USUARIO
    )
    bio = models.TextField(
        'Biografia',
        blank=True,
        null=True
    )
    avatar = models.CharField(
        'Avatar',
        max_length=255,
        blank=True,
        null=True
    )
    status = models.IntegerField(
        'Status',
        choices=choices.PERFIL_STATUS_OPCOES,
        default=choices.PERFIL_STATUS_ATIVO
    )
    
    class Meta:
        db_table = 'profiles'
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "tipo"], name="unique_profile_user_constraint"
            )
        ]
    
    def __str__(self):
        return f'{self.usuario.nome} - {self.get_tipo_display()}'
