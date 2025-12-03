from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from AppCore.basics.models.models import BaseUserManager, BasicModel, Base404ExceptionManager
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin
from AppCore.core.business.business_mixin import ModelBusinessMixin


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
        extra_fields.setdefault('ativo', True)
        
        return self.create_user(cpf, nome, password, **extra_fields)


class Usuario(ModelHelperMixin, ModelBusinessMixin, PermissionsMixin, AbstractBaseUser, BasicModel):
    """
    Classe base para todos os usuários no sistema.
    
    AUTENTICAÇÃO POR CPF (não email).
    
    Esta é a entidade central do diagrama. Todos os tipos de pessoa
    (Servidor, Terceirizado, Aluno, Estagiário) herdam desta classe.
    
    Relacionamentos:
    - Campus (1) → (*) Usuario
    - Cargo (1) → (*) Usuario
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
        "campus.Campus",
        on_delete=models.PROTECT,
        related_name='usuarios',
        verbose_name='Campus',
    )
    cargo = models.ForeignKey(
        "cargo.Cargo",
        on_delete=models.PROTECT,
        related_name='usuarios',
        verbose_name='Cargo',
        null=True,
        blank=True,
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
    ativo = models.BooleanField(
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
    last_login = models.DateField(
        'Último Login',
        blank=True,
        null=True,
    )

    USERNAME_FIELD = 'cpf'
    REQUIRED_FIELDS = ['nome']

    objects = UsuarioManager()

    class Meta:
        db_table = 'usuarios'
        app_label = 'usuarios'
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usurios'
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
    tempo_expiracao = models.DateTimeField(null=False)
    codigo = models.IntegerField(null=False)
    validado = models.BooleanField(default=False)

    def __str__(self):
        return f"Usuario {self.usuario}, codigo {self.codigo}"

    class Meta:
        db_table = 'password_reset_codes'
        app_label = 'usuarios'
        verbose_name = 'Código de redefinição de senha'
        verbose_name_plural = 'Códigos de redefinição de senha'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "codigo"], name="unique_code_user_constraint"
            )
        ]


class Contato(BasicModel):
    """
    Representa os contatos de um usuário (email, telefone).
    
    Relacionamentos:
    - Usuario (1) → (*) Contato
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='contatos',
        verbose_name='Usuário',
    )
    email = models.EmailField(
        'Email',
        blank=True,
        null=True,
    )
    telefone = models.CharField(
        'Telefone',
        max_length=20,
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'contatos'
        app_label = 'usuarios'
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
        unique_together = ('email', 'usuario'), ('telefone', 'usuario')
        ordering = ['usuario', '-created_at']

    def __str__(self):
        return f'{self.usuario.nome} - {self.email or self.telefone}'


class Endereco(BasicModel):
    """
    Representa os endereços de um usuário.
    
    Relacionamentos:
    - Usuario (1) → (*) Endereco
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='enderecos',
        verbose_name='Usuário',
    )
    logradouro = models.CharField(
        'Logradouro',
        max_length=255,
    )
    bairro = models.CharField(
        'Bairro',
        max_length=255,
    )
    cep = models.CharField(
        'CEP',
        max_length=8,
    )
    num_casa = models.CharField(
        'Número',
        max_length=20,
    )
    cidade = models.CharField(
        'Cidade',
        max_length=255,
    )
    estado = models.CharField(
        'Estado',
        max_length=2,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'enderecos'
        app_label = 'usuarios'
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['usuario', '-created_at']

    def __str__(self):
        return f'{self.usuario.nome} - {self.logradouro}, {self.num_casa}'
