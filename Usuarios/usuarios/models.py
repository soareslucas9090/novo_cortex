from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin
from AppCore.core.business.business_mixin import ModelBusinessMixin

from .business import UsuarioBusiness
from .helpers import UsuarioHelper
from . import choices


class UsuarioManager(BaseUserManager, Base404ExceptionManager):
    """
    Manager customizado para Usuario.
    Combina BaseUserManager (para criação de usuários) com Base404ExceptionManager.
    """
    
    def create_user(self, cpf, nome, password=None, **extra_fields):
        if not cpf:
            raise ValueError('O CPF é obrigatório')
        if not nome:
            raise ValueError('O nome é obrigatório')
        
        user = self.model(
            cpf=cpf,
            nome=nome,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, cpf, nome, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        
        return self.create_user(cpf, nome, password, **extra_fields)


class Usuario(ModelHelperMixin, ModelBusinessMixin, PermissionsMixin, AbstractBaseUser, BasicModel):
    """
    Classe base para todos os usuários no sistema.
    
    AUTENTICAÇÃO POR CPF (não email).
    
    Esta é a entidade central do diagrama. Todos os tipos de pessoa
    (Servidor, Terceirizado, Aluno, Estagiário) herdam desta classe.
    
    Relacionamentos:
    - Campus (1) → (*) Usuario
    - Usuario (1) → (*) Contato
    - Usuario (1) → (*) Endereco
    - Usuario (1) → (*) Matricula
    - Usuario (*) ↔ (*) Setor (via UsuarioSetor)
    
    Herança (subtipos via OneToOne):
    - Usuario ← Servidor
    - Usuario ← Terceirizado
    - Usuario ← Aluno
    - Usuario ← Estagiario
    """
    campus = models.ForeignKey(
        Campus,
        on_delete=models.PROTECT,
        related_name='usuarios',
        verbose_name='Campus',
    )
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    cpf = models.CharField(
        'CPF',
        max_length=11,
        unique=True,
    )
    data_nascimento = models.DateField(
        'Data de Nascimento',
    )
    data_ingresso = models.DateField(
        'Data de Ingresso',
        blank=True,
        null=True,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )
    is_admin = models.BooleanField(
        'Administrador',
        default=False,
    )
    is_staff = models.BooleanField(
        'Equipe',
        default=False,
    )
    is_superuser = models.BooleanField(
        'Superusuário',
        default=False,
    )
    ultimo_login = models.DateField(
        'Último Login',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['nome']

    def __str__(self):
        return f'{self.nome} ({self.cpf})'

    def has_perm(self, perm, obj=None):
        return self.is_superuser or self.is_admin

    def has_module_perms(self, app_label):
        return self.is_superuser or self.is_admin

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
