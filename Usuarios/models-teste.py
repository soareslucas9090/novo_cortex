"""
Models de Teste - Tradução completa do DER e Diagrama de Classes

Este arquivo contém todos os modelos traduzidos do DER para Django Models.
Será usado como referência para criação dos apps e módulos correspondentes.

ATUALIZADO: 28 de novembro de 2025

=============================================================================
ESTRUTURA DE APPS SUGERIDA:
=============================================================================

1. Usuarios (já existe) - Mantém Usuario base (login por CPF)
   - Usuario (AbstractBaseUser) - Login por CPF
   - Contato
   - Endereco
   - Matricula

2. Campus
   - Campus

3. Setores
   - Setor
   - Atividade
   - Funcao
   - UsuarioSetor (tabela associativa Usuario-Setor)

4. Cargos
   - Cargo

5. Empresas
   - Empresa (unificada com InstituicaoExterna)
   - Curso

6. Servidores
   - Servidor

7. Alunos
   - Aluno

8. Terceirizados
   - Terceirizado

9. Estagiarios
   - Estagiario

=============================================================================
RELACIONAMENTOS PRINCIPAIS:
=============================================================================

- Campus (1) → (*) Usuario
- Usuario (1) → (*) Contato
- Usuario (1) → (*) Endereco
- Usuario (1) → (*) Matricula
- Usuario (*) ↔ (*) Setor (via UsuarioSetor)
- Setor (1) → (*) Atividade
- Atividade (1) → (*) Funcao
- Usuario ← Servidor (herança via OneToOne)
- Usuario ← Terceirizado (herança via OneToOne)
- Usuario ← Aluno (herança via OneToOne)
- Usuario ← Estagiario (herança via OneToOne)
- Empresa (1) → (*) Terceirizado
- Empresa (1) → (*) Estagiario
- Curso (1) → (*) Estagiario

=============================================================================
AUTENTICAÇÃO:
=============================================================================

- Login: CPF (não email)
- Criação de usuários: Via JSON por admin (individual ou em lote)
- Não há mais fluxo de auto-cadastro com envio de email

=============================================================================
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone

from AppCore.basics.models.models import BasicModel, Base404ExceptionManager
from AppCore.core.helpers.helpers_mixin import ModelHelperMixin
from AppCore.core.business.business_mixin import ModelBusinessMixin


# =============================================================================
# CHOICES
# =============================================================================

# Status genérico
STATUS_ATIVO = 1
STATUS_INATIVO = 0
STATUS_OPCOES = [
    (STATUS_ATIVO, 'Ativo'),
    (STATUS_INATIVO, 'Inativo'),
]

# Situação do Aluno no Sistema
SITUACAO_ALUNO_MATRICULADO = 'matriculado'
SITUACAO_ALUNO_TRANCADO = 'trancado'
SITUACAO_ALUNO_FORMADO = 'formado'
SITUACAO_ALUNO_DESISTENTE = 'desistente'
SITUACAO_ALUNO_TRANSFERIDO = 'transferido'
SITUACAO_ALUNO_OPCOES = [
    (SITUACAO_ALUNO_MATRICULADO, 'Matriculado'),
    (SITUACAO_ALUNO_TRANCADO, 'Trancado'),
    (SITUACAO_ALUNO_FORMADO, 'Formado'),
    (SITUACAO_ALUNO_DESISTENTE, 'Desistente'),
    (SITUACAO_ALUNO_TRANSFERIDO, 'Transferido'),
]

# Turno do Aluno
TURNO_MATUTINO = 'matutino'
TURNO_VESPERTINO = 'vespertino'
TURNO_NOTURNO = 'noturno'
TURNO_INTEGRAL = 'integral'
TURNO_OPCOES = [
    (TURNO_MATUTINO, 'Matutino'),
    (TURNO_VESPERTINO, 'Vespertino'),
    (TURNO_NOTURNO, 'Noturno'),
    (TURNO_INTEGRAL, 'Integral'),
]

# Forma de Ingresso do Aluno
FORMA_INGRESSO_VESTIBULAR = 'vestibular'
FORMA_INGRESSO_ENEM = 'enem'
FORMA_INGRESSO_TRANSFERENCIA = 'transferencia'
FORMA_INGRESSO_REINGRESSO = 'reingresso'
FORMA_INGRESSO_OPCOES = [
    (FORMA_INGRESSO_VESTIBULAR, 'Vestibular'),
    (FORMA_INGRESSO_ENEM, 'ENEM/SISU'),
    (FORMA_INGRESSO_TRANSFERENCIA, 'Transferência'),
    (FORMA_INGRESSO_REINGRESSO, 'Reingresso'),
]

# Jornada de Trabalho do Servidor
JORNADA_20 = 20
JORNADA_40 = 40
JORNADA_DE = 0  # Dedicação Exclusiva (representado como 0 para indicar DE)
JORNADA_OPCOES = [
    (JORNADA_20, '20 horas'),
    (JORNADA_40, '40 horas'),
    (JORNADA_DE, 'Dedicação Exclusiva'),
]


# =============================================================================
# MODELS - CAMPUS
# =============================================================================

class Campus(BasicModel):
    """
    Representa um campus da instituição.
    
    Relacionamentos:
    - Campus (1) → (*) Usuario
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    cnpj = models.CharField(
        'CNPJ',
        max_length=14,
        unique=True,
    )
    ativo = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'campus'
        verbose_name = 'Campus'
        verbose_name_plural = 'Campi'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# =============================================================================
# MODELS - CARGO
# =============================================================================

class Cargo(BasicModel):
    """
    Representa um cargo na instituição.
    
    Entidade simples sem relacionamentos diretos no DER.
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
        unique=True,
    )
    ativo = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'cargos'
        verbose_name = 'Cargo'
        verbose_name_plural = 'Cargos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# =============================================================================
# MODELS - EMPRESA E CURSO
# =============================================================================

class Empresa(BasicModel):
    """
    Representa uma empresa (terceirizada ou instituição externa).
    
    Unifica Empresa e InstituicaoExterna do DER anterior.
    
    Relacionamentos:
    - Empresa (1) → (*) Terceirizado
    - Empresa (1) → (*) Estagiario
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    cnpj = models.CharField(
        'CNPJ',
        max_length=14,
        unique=True,
    )
    ativo = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'empresas'
        verbose_name = 'Empresa/Instituição'
        verbose_name_plural = 'Empresas/Instituições'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Curso(BasicModel):
    """
    Representa um curso (para estagiários).
    
    Relacionamentos:
    - Curso (1) → (*) Estagiario
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    descricao = models.TextField(
        'Descrição',
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'cursos'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# =============================================================================
# MODELS - SETOR, ATIVIDADE E FUNÇÃO
# =============================================================================

class Setor(BasicModel):
    """
    Representa um setor dentro do campus.
    
    Relacionamentos:
    - Setor (1) → (*) Atividade
    - Setor (*) ↔ (*) Usuario (via UsuarioSetor)
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    ativo = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'setores'
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Atividade(BasicModel):
    """
    Representa uma atividade dentro de um setor.
    
    Relacionamentos:
    - Setor (1) → (*) Atividade
    - Atividade (1) → (*) Funcao
    """
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        related_name='atividades',
        verbose_name='Setor',
    )
    descricao = models.TextField(
        'Descrição',
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'atividades'
        verbose_name = 'Atividade'
        verbose_name_plural = 'Atividades'
        ordering = ['setor', 'descricao']

    def __str__(self):
        return f'{self.setor.nome} - {self.descricao[:50]}'


class Funcao(BasicModel):
    """
    Representa uma função dentro de uma atividade.
    
    Relacionamentos:
    - Atividade (1) → (*) Funcao
    """
    atividade = models.ForeignKey(
        Atividade,
        on_delete=models.PROTECT,
        related_name='funcoes',
        verbose_name='Atividade',
    )
    descricao = models.TextField(
        'Descrição',
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'funcoes'
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'
        ordering = ['atividade', 'descricao']

    def __str__(self):
        return f'{self.atividade.setor.nome} - {self.descricao[:50]}'


# =============================================================================
# CUSTOM USER MANAGER
# =============================================================================

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


# =============================================================================
# MODELS - USUARIO (BASE - Autenticação por CPF)
# =============================================================================

class Usuario(AbstractBaseUser, BasicModel):
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
    ultimo_login = models.DateField(
        'Último Login',
        blank=True,
        null=True,
    )

    # Configuração do AbstractBaseUser
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


# =============================================================================
# MODELS - USUARIO_SETOR (Tabela Associativa)
# =============================================================================

class UsuarioSetor(BasicModel):
    """
    Tabela associativa entre Usuario e Setor.
    
    Representa a associação de um usuário a um setor, com informações
    sobre responsabilidade, monitor e datas.
    
    Relacionamentos:
    - Usuario (*) ↔ (*) Setor
    - UsuarioSetor → Campus (referência ao campus do setor)
    """
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='usuario_setores',
        verbose_name='Usuário',
    )
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        related_name='usuario_setores',
        verbose_name='Setor',
    )
    campus = models.ForeignKey(
        Campus,
        on_delete=models.PROTECT,
        related_name='usuario_setores',
        verbose_name='Campus',
    )
    e_responsavel = models.BooleanField(
        'É Responsável',
        default=False,
    )
    monitor = models.BooleanField(
        'Monitor',
        default=False,
    )
    data_entrada = models.DateField(
        'Data de Entrada',
        default=timezone.now,
    )
    data_saida = models.DateField(
        'Data de Saída',
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'usuario_setor'
        verbose_name = 'Usuário-Setor'
        verbose_name_plural = 'Usuários-Setores'
        ordering = ['usuario', 'setor']
        constraints = [
            models.UniqueConstraint(
                fields=['usuario', 'setor'],
                name='unique_usuario_setor'
            )
        ]

    def __str__(self):
        return f'{self.usuario.nome} - {self.setor.nome}'


# =============================================================================
# MODELS - CONTATO, ENDEREÇO E MATRÍCULA (Relacionados a Usuario)
# =============================================================================

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
        verbose_name = 'Contato'
        verbose_name_plural = 'Contatos'
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
        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'
        ordering = ['usuario', '-created_at']

    def __str__(self):
        return f'{self.usuario.nome} - {self.logradouro}, {self.num_casa}'


class Matricula(BasicModel):
    """
    Representa as matrículas/carteirinhas de um usuário.
    
    Relacionamentos:
    - Usuario (1) → (*) Matricula
    """
    matricula = models.CharField(
        'Número da Matrícula',
        max_length=50,
        unique=True,
        primary_key=True,
    )
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='matriculas',
        verbose_name='Usuário',
    )
    data_validade = models.DateField(
        'Data de Validade',
    )
    data_expedicao = models.DateField(
        'Data de Expedição',
        default=timezone.now,
    )
    ativo = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'matriculas'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        ordering = ['usuario', '-data_expedicao']

    def __str__(self):
        return f'{self.usuario.nome} - {self.matricula}'


# =============================================================================
# MODELS - SERVIDOR (Herança de Usuario)
# =============================================================================

class Servidor(BasicModel):
    """
    Representa um servidor da instituição.
    
    Herança via OneToOne:
    - Usuario ← Servidor
    
    Campos do DER:
    - data_posse
    - jornada_trabalho (INTEGER)
    - padrao (VARCHAR)
    - classe (VARCHAR)
    - tipo_servidor (VARCHAR)
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='servidor',
        verbose_name='Usuário',
        primary_key=True,
    )
    data_posse = models.DateField(
        'Data de Posse',
    )
    jornada_trabalho = models.IntegerField(
        'Jornada de Trabalho',
        choices=JORNADA_OPCOES,
        default=JORNADA_40,
        help_text='Horas semanais (0 = Dedicação Exclusiva)',
    )
    padrao = models.CharField(
        'Padrão',
        max_length=50,
    )
    classe = models.CharField(
        'Classe',
        max_length=50,
    )
    tipo_servidor = models.CharField(
        'Tipo de Servidor',
        max_length=100,
        help_text='Ex: Professor, Técnico Administrativo, etc.',
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'servidores'
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'
        ordering = ['usuario__nome']

    def __str__(self):
        return f'{self.usuario.nome} - {self.tipo_servidor}'


# =============================================================================
# MODELS - TERCEIRIZADO (Herança de Usuario)
# =============================================================================

class Terceirizado(BasicModel):
    """
    Representa um funcionário terceirizado.
    
    Herança via OneToOne:
    - Usuario ← Terceirizado
    
    Relacionamentos:
    - Empresa (1) → (*) Terceirizado
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='terceirizado',
        verbose_name='Usuário',
        primary_key=True,
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name='terceirizados',
        verbose_name='Empresa',
    )
    data_inicio_contrato = models.DateField(
        'Data de Início do Contrato',
    )
    data_fim_contrato = models.DateField(
        'Data de Fim do Contrato',
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'terceirizados'
        verbose_name = 'Terceirizado'
        verbose_name_plural = 'Terceirizados'
        ordering = ['usuario__nome']

    def __str__(self):
        return f'{self.usuario.nome} - {self.empresa.nome}'


# =============================================================================
# MODELS - ALUNO (Herança de Usuario)
# =============================================================================

class Aluno(BasicModel):
    """
    Representa um aluno da instituição.
    
    Herança via OneToOne:
    - Usuario ← Aluno
    
    Campos do DER:
    - ira (DOUBLE)
    - forma_ingresso (VARCHAR)
    - previsao_conclusao (INTEGER)
    - aluno_especial (BOOLEAN)
    - turno (VARCHAR)
    - ativo (BOOLEAN)
    - ano_conclusao (INTEGER)
    - data_colacao (DATE)
    - data_expedicao_diploma (DATE)
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='aluno',
        verbose_name='Usuário',
        primary_key=True,
    )
    ira = models.DecimalField(
        'IRA',
        max_digits=4,
        decimal_places=2,
        default=0.00,
        help_text='Índice de Rendimento Acadêmico (0.00 a 10.00)',
    )
    forma_ingresso = models.CharField(
        'Forma de Ingresso',
        max_length=20,
        choices=FORMA_INGRESSO_OPCOES,
        default=FORMA_INGRESSO_ENEM,
    )
    previsao_conclusao = models.IntegerField(
        'Previsão de Conclusão',
        help_text='Ano previsto para conclusão do curso',
    )
    aluno_especial = models.BooleanField(
        'Aluno Especial',
        default=False,
    )
    turno = models.CharField(
        'Turno',
        max_length=20,
        choices=TURNO_OPCOES,
        default=TURNO_INTEGRAL,
    )
    ativo = models.BooleanField(
        'Ativo',
        default=True,
    )
    # Campos de conclusão (quando o aluno se forma)
    ano_conclusao = models.IntegerField(
        'Ano de Conclusão',
        blank=True,
        null=True,
    )
    data_colacao = models.DateField(
        'Data de Colação',
        blank=True,
        null=True,
    )
    data_expedicao_diploma = models.DateField(
        'Data de Expedição do Diploma',
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'alunos'
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['usuario__nome']

    def __str__(self):
        return f'{self.usuario.nome} - IRA: {self.ira}'

    @property
    def is_formado(self):
        """Verifica se o aluno já se formou."""
        return self.ano_conclusao is not None


# =============================================================================
# MODELS - ESTAGIÁRIO (Herança de Usuario)
# =============================================================================

class Estagiario(BasicModel):
    """
    Representa um estagiário na instituição.
    
    Herança via OneToOne:
    - Usuario ← Estagiario
    
    Relacionamentos:
    - Empresa (1) → (*) Estagiario
    - Curso (1) → (*) Estagiario
    
    Campos do DER:
    - carga_horaria (INTEGER)
    - data_inicio_estagio (DATE)
    - data_fim_estagio (DATE)
    """
    usuario = models.OneToOneField(
        Usuario,
        on_delete=models.CASCADE,
        related_name='estagiario',
        verbose_name='Usuário',
        primary_key=True,
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name='estagiarios',
        verbose_name='Empresa/Instituição',
    )
    curso = models.ForeignKey(
        Curso,
        on_delete=models.PROTECT,
        related_name='estagiarios',
        verbose_name='Curso',
    )
    carga_horaria = models.IntegerField(
        'Carga Horária',
        help_text='Carga horária semanal do estágio',
    )
    data_inicio_estagio = models.DateField(
        'Data de Início do Estágio',
    )
    data_fim_estagio = models.DateField(
        'Data de Fim do Estágio',
        blank=True,
        null=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'estagiarios'
        verbose_name = 'Estagiário'
        verbose_name_plural = 'Estagiários'
        ordering = ['usuario__nome']

    def __str__(self):
        return f'{self.usuario.nome} - {self.curso.nome}'


# =============================================================================
# RESUMO DOS MODELOS E APPS SUGERIDOS
# =============================================================================
"""
=============================================================================
RESUMO PARA CRIAÇÃO DOS APPS
=============================================================================

1. APP: usuarios (já existe - adaptar)
   - Models: Usuario (login por CPF), Contato, Endereco, Matricula
   - Dependências: campus

2. APP: campus
   - Models: Campus
   - Dependências: Nenhuma

3. APP: cargos
   - Models: Cargo
   - Dependências: Nenhuma

4. APP: empresas
   - Models: Empresa, Curso
   - Dependências: Nenhuma

5. APP: setores
   - Models: Setor, Atividade, Funcao, UsuarioSetor
   - Dependências: usuarios, campus

6. APP: servidores
   - Models: Servidor
   - Dependências: usuarios

7. APP: alunos
   - Models: Aluno
   - Dependências: usuarios

8. APP: terceirizados
   - Models: Terceirizado
   - Dependências: usuarios, empresas

9. APP: estagiarios
   - Models: Estagiario
   - Dependências: usuarios, empresas

=============================================================================
ORDEM DE CRIAÇÃO SUGERIDA (Baseada nas dependências):
=============================================================================

1. campus (sem dependências)
2. cargos (sem dependências)
3. empresas (sem dependências) - inclui Empresa e Curso
4. usuarios (depende de campus) - Usuario, Contato, Endereco, Matricula
5. setores (depende de usuarios, campus) - Setor, Atividade, Funcao, UsuarioSetor
6. servidores (depende de usuarios)
7. alunos (depende de usuarios)
8. terceirizados (depende de usuarios, empresas)
9. estagiarios (depende de usuarios, empresas)

=============================================================================
DIAGRAMA DE HERANÇA (RESUMO):
=============================================================================

                    Usuario
                       │
        ┌──────────────┼──────────────┬──────────────┐
        │              │              │              │
    Servidor      Terceirizado     Aluno       Estagiario

=============================================================================
RELACIONAMENTOS MANY-TO-MANY:
=============================================================================

Usuario ←──[UsuarioSetor]──→ Setor
           │
           └── e_responsavel, monitor, data_entrada, data_saida, campus

=============================================================================
AUTENTICAÇÃO:
=============================================================================

- USERNAME_FIELD = 'cpf'
- Criação de usuários via JSON por admin (não auto-cadastro)
- Suporte a criação individual ou em lote

=============================================================================
"""
