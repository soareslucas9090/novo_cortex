"""
Models de Teste - Tradução completa do DER e Diagrama de Classes

Este arquivo contém todos os modelos traduzidos do DER para Django Models.
Será usado como referência para criação dos apps e módulos correspondentes.

=============================================================================
ESTRUTURA DE APPS SUGERIDA:
=============================================================================

1. Usuarios (já existe) - Mantém Usuario base
   - Usuario (AbstractBaseUser) - JÁ IMPLEMENTADO
   - Pessoa (extensão do Usuario com dados específicos do contexto acadêmico)

2. Campus
   - Campus

3. Pessoas
   - Pessoa (base)
   - Servidor
   - Professor
   - TecnicoAdministrativo
   - Aluno
   - Egresso
   - Estagiario
   - Terceirizado
   - Contato
   - Endereco
   - Matricula

4. Setores
   - Setor
   - Funcao
   - PessoaFuncao

5. Empresas
   - Empresa
   - InstituicaoExterna

=============================================================================
RELACIONAMENTOS PRINCIPAIS:
=============================================================================

- Campus (1) → (*) Pessoa
- Pessoa (1) → (*) Contato
- Pessoa (1) → (*) Endereco
- Pessoa (1) → (*) Matricula
- Pessoa (1) → (*) PessoaFuncao
- Funcao (1) → (*) PessoaFuncao
- Setor (1) → (*) Funcao
- Pessoa ← Servidor (herança)
- Pessoa ← Terceirizado (herança)
- Pessoa ← Aluno (herança)
- Pessoa ← Estagiario (herança)
- Servidor ← Professor (herança)
- Servidor ← TecnicoAdministrativo (herança)
- Aluno ← Egresso (herança)
- Empresa (1) → (*) Terceirizado
- InstituicaoExterna (1) → (*) Estagiario

=============================================================================
"""

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

# Forma de Ingresso
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

# Carga Horária do Servidor
CARGA_HORARIA_20 = '20h'
CARGA_HORARIA_40 = '40h'
CARGA_HORARIA_DE = 'de'  # Dedicação Exclusiva
CARGA_HORARIA_OPCOES = [
    (CARGA_HORARIA_20, '20 horas'),
    (CARGA_HORARIA_40, '40 horas'),
    (CARGA_HORARIA_DE, 'Dedicação Exclusiva'),
]

# Título do Professor
TITULO_GRADUADO = 'graduado'
TITULO_ESPECIALISTA = 'especialista'
TITULO_MESTRE = 'mestre'
TITULO_DOUTOR = 'doutor'
TITULO_POS_DOUTOR = 'pos_doutor'
TITULO_OPCOES = [
    (TITULO_GRADUADO, 'Graduado'),
    (TITULO_ESPECIALISTA, 'Especialista'),
    (TITULO_MESTRE, 'Mestre'),
    (TITULO_DOUTOR, 'Doutor'),
    (TITULO_POS_DOUTOR, 'Pós-Doutor'),
]

# Classe do Professor
CLASSE_D = 'd'
CLASSE_C = 'c'
CLASSE_B = 'b'
CLASSE_A = 'a'
CLASSE_TITULAR = 'titular'
CLASSE_OPCOES = [
    (CLASSE_D, 'Classe D'),
    (CLASSE_C, 'Classe C'),
    (CLASSE_B, 'Classe B'),
    (CLASSE_A, 'Classe A'),
    (CLASSE_TITULAR, 'Titular'),
]

# Nível Técnico Administrativo
NIVEL_A = 'a'
NIVEL_B = 'b'
NIVEL_C = 'c'
NIVEL_D = 'd'
NIVEL_E = 'e'
NIVEL_OPCOES = [
    (NIVEL_A, 'Nível A'),
    (NIVEL_B, 'Nível B'),
    (NIVEL_C, 'Nível C'),
    (NIVEL_D, 'Nível D'),
    (NIVEL_E, 'Nível E'),
]


# =============================================================================
# MODELS - CAMPUS
# =============================================================================

class Campus(BasicModel):
    """
    Representa um campus da instituição.
    
    Relacionamentos:
    - Campus (1) → (*) Pessoa
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
    codigo_campus = models.CharField(
        'Código do Campus',
        max_length=50,
        unique=True,
    )
    is_active = models.BooleanField(
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
# MODELS - EMPRESA E INSTITUIÇÃO EXTERNA
# =============================================================================

class Empresa(BasicModel):
    """
    Representa uma empresa terceirizada.
    
    Relacionamentos:
    - Empresa (1) → (*) Terceirizado
    """
    cnpj = models.CharField(
        'CNPJ',
        max_length=14,
        unique=True,
        primary_key=True,
    )
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'empresas'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class InstituicaoExterna(BasicModel):
    """
    Representa uma instituição externa (para estagiários).
    
    Relacionamentos:
    - InstituicaoExterna (1) → (*) Estagiario
    """
    cnpj = models.CharField(
        'CNPJ',
        max_length=14,
        unique=True,
        primary_key=True,
    )
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'instituicoes_externas'
        verbose_name = 'Instituição Externa'
        verbose_name_plural = 'Instituições Externas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# =============================================================================
# MODELS - SETOR E FUNÇÃO
# =============================================================================

class Setor(BasicModel):
    """
    Representa um setor dentro de um campus.
    
    Relacionamentos:
    - Setor (1) → (*) Funcao
    
    Exemplos (conforme diagrama):
    - Setor de Saúde → Médico, Enfermeiro, Odontologista
    - Direção → Diretor de ensino, Diretor geral
    - Coordenações → Coordenador de TADS, Biologia, Matemática
    - Rádio → Monitor da Rádio
    """
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    is_active = models.BooleanField(
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


class Funcao(BasicModel):
    """
    Representa uma função dentro de um setor.
    
    Relacionamentos:
    - Setor (1) → (*) Funcao
    - Funcao (1) → (*) PessoaFuncao
    
    Exemplos (conforme diagrama):
    - Setor de Saúde: Médico, Enfermeiro, Odontologista
    - Direção: Diretor de ensino, Diretor geral
    - Coordenações: Coordenador de TADS, Coordenador de Biologia
    - Rádio: Monitor da Rádio
    - Geral: Professor
    """
    setor = models.ForeignKey(
        Setor,
        on_delete=models.PROTECT,
        related_name='funcoes',
        verbose_name='Setor',
    )
    nome = models.CharField(
        'Nome',
        max_length=255,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'funcoes'
        verbose_name = 'Função'
        verbose_name_plural = 'Funções'
        ordering = ['setor', 'nome']
        constraints = [
            models.UniqueConstraint(
                fields=['setor', 'nome'],
                name='unique_funcao_por_setor'
            )
        ]

    def __str__(self):
        return f'{self.nome} - {self.setor.nome}'


# =============================================================================
# MODELS - PESSOA (BASE)
# =============================================================================

class Pessoa(BasicModel):
    """
    Classe base para todas as pessoas no sistema.
    
    Esta é a entidade central do diagrama. Todas as pessoas (Servidor, 
    Terceirizado, Aluno, Estagiário) herdam desta classe.
    
    Relacionamentos:
    - Campus (1) → (*) Pessoa
    - Pessoa (1) → (*) Contato
    - Pessoa (1) → (*) Endereco
    - Pessoa (1) → (*) Matricula
    - Pessoa (1) → (*) PessoaFuncao
    
    Herança (subtipos):
    - Pessoa ← Servidor
    - Pessoa ← Terceirizado
    - Pessoa ← Aluno
    - Pessoa ← Estagiario
    """
    campus = models.ForeignKey(
        Campus,
        on_delete=models.PROTECT,
        related_name='pessoas',
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
    data_de_nascimento = models.DateField(
        'Data de Nascimento',
    )
    data_ingresso = models.DateField(
        'Data de Ingresso',
        default=timezone.now,
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

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'pessoas'
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        ordering = ['nome']

    def __str__(self):
        return self.nome


# =============================================================================
# MODELS - CONTATO, ENDEREÇO E MATRÍCULA (Relacionados a Pessoa)
# =============================================================================

class Contato(BasicModel):
    """
    Representa os contatos de uma pessoa (email, telefone).
    
    Relacionamentos:
    - Pessoa (1) → (*) Contato
    """
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='contatos',
        verbose_name='Pessoa',
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
        ordering = ['pessoa', '-created_at']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.email or self.telefone}'


class Endereco(BasicModel):
    """
    Representa os endereços de uma pessoa.
    
    Relacionamentos:
    - Pessoa (1) → (*) Endereco
    """
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='enderecos',
        verbose_name='Pessoa',
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
    complemento = models.CharField(
        'Complemento',
        max_length=255,
        blank=True,
        null=True,
    )
    num_casa = models.IntegerField(
        'Número',
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
        ordering = ['pessoa', '-created_at']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.logradouro}, {self.num_casa}'


class Matricula(BasicModel):
    """
    Representa as matrículas/carteirinhas de uma pessoa.
    
    Relacionamentos:
    - Pessoa (1) → (*) Matricula
    """
    matricula = models.CharField(
        'Número da Matrícula',
        max_length=50,
        unique=True,
        primary_key=True,
    )
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='matriculas',
        verbose_name='Pessoa',
    )
    data_validade = models.DateField(
        'Data de Validade',
    )
    data_expedicao = models.DateField(
        'Data de Expedição',
        default=timezone.now,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'matriculas'
        verbose_name = 'Matrícula'
        verbose_name_plural = 'Matrículas'
        ordering = ['pessoa', '-data_expedicao']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.matricula}'


# =============================================================================
# MODELS - PESSOA_FUNCAO (Tabela Associativa)
# =============================================================================

class PessoaFuncao(BasicModel):
    """
    Tabela associativa entre Pessoa e Função.
    
    Representa as funções que uma pessoa exerce em setores específicos.
    
    Relacionamentos:
    - Pessoa (1) → (*) PessoaFuncao
    - Funcao (1) → (*) PessoaFuncao
    
    Atributos próprios:
    - setores_e_funcoes: dict relacionando setores e funções
    - data_inicio: quando a pessoa começou a exercer a função
    - is_active: se a função ainda está ativa
    """
    pessoa = models.ForeignKey(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='pessoa_funcoes',
        verbose_name='Pessoa',
    )
    funcao = models.ForeignKey(
        Funcao,
        on_delete=models.PROTECT,
        related_name='pessoa_funcoes',
        verbose_name='Função',
    )
    setores_e_funcoes = models.JSONField(
        'Setores e Funções',
        default=dict,
        blank=True,
        help_text='Dict com mapeamento de setores e funções exercidas',
    )
    data_inicio = models.DateField(
        'Data de Início',
        default=timezone.now,
    )
    is_active = models.BooleanField(
        'Ativo',
        default=True,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'pessoa_funcoes'
        verbose_name = 'Pessoa-Função'
        verbose_name_plural = 'Pessoas-Funções'
        ordering = ['pessoa', 'funcao']
        constraints = [
            models.UniqueConstraint(
                fields=['pessoa', 'funcao'],
                name='unique_pessoa_funcao'
            )
        ]

    def __str__(self):
        return f'{self.pessoa.nome} - {self.funcao.nome}'


# =============================================================================
# MODELS - SERVIDOR (Herança de Pessoa)
# =============================================================================

class Servidor(BasicModel):
    """
    Representa um servidor da instituição.
    
    Herança:
    - Pessoa ← Servidor
    
    Subtipos:
    - Servidor ← Professor
    - Servidor ← TecnicoAdministrativo
    """
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='servidor',
        verbose_name='Pessoa',
        primary_key=True,
    )
    numero_siape = models.CharField(
        'Número SIAPE',
        max_length=20,
        unique=True,
    )
    data_admissao = models.DateField(
        'Data de Admissão',
    )
    salario_base = models.DecimalField(
        'Salário Base',
        max_digits=10,
        decimal_places=2,
    )
    carga_horaria = models.CharField(
        'Carga Horária',
        max_length=10,
        choices=CARGA_HORARIA_OPCOES,
        default=CARGA_HORARIA_40,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'servidores'
        verbose_name = 'Servidor'
        verbose_name_plural = 'Servidores'
        ordering = ['pessoa__nome']

    def __str__(self):
        return f'{self.pessoa.nome} - SIAPE: {self.numero_siape}'


class Professor(BasicModel):
    """
    Representa um professor (subtipo de Servidor).
    
    Herança:
    - Servidor ← Professor
    """
    servidor = models.OneToOneField(
        Servidor,
        on_delete=models.CASCADE,
        related_name='professor',
        verbose_name='Servidor',
        primary_key=True,
    )
    titulo = models.CharField(
        'Título',
        max_length=20,
        choices=TITULO_OPCOES,
        default=TITULO_GRADUADO,
    )
    area_atuacao = models.CharField(
        'Área de Atuação',
        max_length=255,
    )
    classe = models.CharField(
        'Classe',
        max_length=20,
        choices=CLASSE_OPCOES,
        default=CLASSE_D,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'professores'
        verbose_name = 'Professor'
        verbose_name_plural = 'Professores'
        ordering = ['servidor__pessoa__nome']

    def __str__(self):
        return f'Prof. {self.servidor.pessoa.nome} - {self.get_titulo_display()}'


class TecnicoAdministrativo(BasicModel):
    """
    Representa um técnico administrativo (subtipo de Servidor).
    
    Herança:
    - Servidor ← TecnicoAdministrativo
    """
    servidor = models.OneToOneField(
        Servidor,
        on_delete=models.CASCADE,
        related_name='tecnico_administrativo',
        verbose_name='Servidor',
        primary_key=True,
    )
    nivel = models.CharField(
        'Nível',
        max_length=5,
        choices=NIVEL_OPCOES,
        default=NIVEL_D,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'tecnicos_administrativos'
        verbose_name = 'Técnico Administrativo'
        verbose_name_plural = 'Técnicos Administrativos'
        ordering = ['servidor__pessoa__nome']

    def __str__(self):
        return f'{self.servidor.pessoa.nome} - {self.get_nivel_display()}'


# =============================================================================
# MODELS - TERCEIRIZADO (Herança de Pessoa)
# =============================================================================

class Terceirizado(BasicModel):
    """
    Representa um funcionário terceirizado.
    
    Herança:
    - Pessoa ← Terceirizado
    
    Relacionamentos:
    - Empresa (1) → (*) Terceirizado
    """
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='terceirizado',
        verbose_name='Pessoa',
        primary_key=True,
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.PROTECT,
        related_name='terceirizados',
        verbose_name='Empresa',
    )
    matricula_externa = models.CharField(
        'Matrícula Externa',
        max_length=50,
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
        ordering = ['pessoa__nome']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.empresa.nome}'


# =============================================================================
# MODELS - ALUNO (Herança de Pessoa)
# =============================================================================

class Aluno(BasicModel):
    """
    Representa um aluno da instituição.
    
    Herança:
    - Pessoa ← Aluno
    
    Subtipos:
    - Aluno ← Egresso
    
    Relacionamentos:
    - Aluno (1) → (*) Estagiario (um aluno pode ter vários estágios)
    """
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='aluno',
        verbose_name='Pessoa',
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
    situacao_sistema = models.CharField(
        'Situação no Sistema',
        max_length=20,
        choices=SITUACAO_ALUNO_OPCOES,
        default=SITUACAO_ALUNO_MATRICULADO,
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'alunos'
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
        ordering = ['pessoa__nome']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.get_situacao_sistema_display()}'


class Egresso(BasicModel):
    """
    Representa um ex-aluno (egresso) da instituição.
    
    Herança:
    - Aluno ← Egresso
    
    Um egresso é um aluno que já concluiu o curso.
    """
    aluno = models.OneToOneField(
        Aluno,
        on_delete=models.CASCADE,
        related_name='egresso',
        verbose_name='Aluno',
        primary_key=True,
    )
    ano_conclusao = models.IntegerField(
        'Ano de Conclusão',
    )
    data_formatura = models.DateField(
        'Data de Formatura',
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'egressos'
        verbose_name = 'Egresso'
        verbose_name_plural = 'Egressos'
        ordering = ['aluno__pessoa__nome']

    def __str__(self):
        return f'{self.aluno.pessoa.nome} - Formado em {self.ano_conclusao}'


# =============================================================================
# MODELS - ESTAGIÁRIO (Herança de Pessoa, relacionado a Aluno)
# =============================================================================

class Estagiario(BasicModel):
    """
    Representa um estagiário na instituição.
    
    Herança:
    - Pessoa ← Estagiario
    
    Relacionamentos:
    - Aluno (1) → (*) Estagiario (um aluno pode ter vários estágios)
    - InstituicaoExterna (1) → (*) Estagiario
    
    Nota: Estagiário é um papel que uma pessoa (geralmente aluno) pode ter,
    não necessariamente herança direta de Aluno conforme o DER.
    """
    pessoa = models.OneToOneField(
        Pessoa,
        on_delete=models.CASCADE,
        related_name='estagiario',
        verbose_name='Pessoa',
        primary_key=True,
    )
    instituicao_externa = models.ForeignKey(
        InstituicaoExterna,
        on_delete=models.PROTECT,
        related_name='estagiarios',
        verbose_name='Instituição Externa',
    )
    matricula_externa = models.CharField(
        'Matrícula Externa',
        max_length=50,
    )
    curso = models.CharField(
        'Curso',
        max_length=255,
    )
    carga_horaria = models.IntegerField(
        'Carga Horária',
        help_text='Carga horária semanal do estágio',
    )
    data_inicio = models.DateField(
        'Data de Início',
    )
    data_fim = models.DateField(
        'Data de Fim',
    )

    objects = Base404ExceptionManager()

    class Meta:
        db_table = 'estagiarios'
        verbose_name = 'Estagiário'
        verbose_name_plural = 'Estagiários'
        ordering = ['pessoa__nome']

    def __str__(self):
        return f'{self.pessoa.nome} - {self.curso}'


# =============================================================================
# RESUMO DOS MODELOS E APPS SUGERIDOS
# =============================================================================
"""
=============================================================================
RESUMO PARA CRIAÇÃO DOS APPS
=============================================================================

1. APP: campus
   - Models: Campus
   - Dependências: Nenhuma

2. APP: empresas
   - Models: Empresa, InstituicaoExterna
   - Dependências: Nenhuma

3. APP: setores
   - Models: Setor, Funcao
   - Dependências: Nenhuma

4. APP: pessoas
   - Models: Pessoa, Contato, Endereco, Matricula, PessoaFuncao
   - Dependências: campus, setores

5. APP: servidores
   - Models: Servidor, Professor, TecnicoAdministrativo
   - Dependências: pessoas

6. APP: alunos
   - Models: Aluno, Egresso
   - Dependências: pessoas

7. APP: terceirizados
   - Models: Terceirizado
   - Dependências: pessoas, empresas

8. APP: estagiarios
   - Models: Estagiario
   - Dependências: pessoas, empresas

=============================================================================
ORDEM DE CRIAÇÃO SUGERIDA (Baseada nas dependências):
=============================================================================

1. campus (sem dependências)
2. empresas (sem dependências)  
3. setores (sem dependências)
4. pessoas (depende de campus, setores)
5. servidores (depende de pessoas)
6. alunos (depende de pessoas)
7. terceirizados (depende de pessoas, empresas)
8. estagiarios (depende de pessoas, empresas)

=============================================================================
DIAGRAMA DE HERANÇA (RESUMO):
=============================================================================

                    Pessoa
                       │
        ┌──────────────┼──────────────┐
        │              │              │
    Servidor      Terceirizado     Aluno ────── Estagiario
        │                             │
   ┌────┴────┐                    Egresso
   │         │
Professor  TecnicoAdministrativo

=============================================================================
"""
