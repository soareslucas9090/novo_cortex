from rest_framework import serializers

from Usuarios.usuario.serializers import (
    CampusResumoSerializer,
    ContatoListaSerializer,
    EnderecoListaSerializer,
    UsuarioSetorResumoSerializer,
)

from . import choices


# ============================================================================
# SERIALIZERS DE USUÁRIO BASE PARA ALUNO
# ============================================================================

class UsuarioBaseAlunoSerializer(serializers.Serializer):
    """
    Serializer do usuário base para uso nos serializers de Aluno.
    
    Inclui dados básicos do usuário sem os perfis para evitar
    referência circular.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cpf = serializers.CharField(read_only=True)
    cpf_formatado = serializers.SerializerMethodField()
    data_nascimento = serializers.DateField(read_only=True)
    data_ingresso = serializers.DateField(read_only=True, allow_null=True)
    ativo = serializers.BooleanField(read_only=True)
    campus = CampusResumoSerializer(read_only=True)

    def get_cpf_formatado(self, obj):
        """Retorna o CPF formatado (XXX.XXX.XXX-XX)."""
        cpf = obj.cpf
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf


class UsuarioCompletoAlunoSerializer(UsuarioBaseAlunoSerializer):
    """
    Serializer completo do usuário base para Aluno.
    
    Inclui contatos, endereços e setores.
    """
    contatos = ContatoListaSerializer(many=True, read_only=True)
    enderecos = EnderecoListaSerializer(many=True, read_only=True)
    setores = serializers.SerializerMethodField()

    def get_setores(self, obj):
        """Retorna os setores vinculados ao usuário."""
        usuario_setores = obj.usuario_setores.select_related('setor', 'campus').all()
        return UsuarioSetorResumoSerializer(usuario_setores, many=True).data


# ============================================================================
# SERIALIZERS DE ALUNO
# ============================================================================

class AlunoListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de alunos (versão resumida).
    
    Ideal para endpoints de listagem onde não é necessário
    carregar todos os dados relacionados.
    """
    # Identificação (usa o pk do usuário)
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    cpf = serializers.CharField(source='usuario.cpf', read_only=True)
    
    # Dados do aluno
    ira = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    turno = serializers.CharField(read_only=True)
    turno_display = serializers.SerializerMethodField()
    previsao_conclusao = serializers.IntegerField(read_only=True)
    aluno_especial = serializers.BooleanField(read_only=True)
    
    # Campus do usuário
    campus = CampusResumoSerializer(source='usuario.campus', read_only=True)
    
    # Status
    ativo = serializers.BooleanField(read_only=True)
    is_formado = serializers.BooleanField(read_only=True)

    def get_turno_display(self, obj):
        """Retorna a descrição legível do turno."""
        return obj.get_turno_display()


class AlunoDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um aluno.
    
    Inclui:
    - Dados específicos do aluno
    - Informações completas do usuário base
    - Contatos e endereços
    - Setores vinculados
    - Dados de conclusão (se formado)
    """
    # Identificação
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    
    # Dados acadêmicos
    ira = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    forma_ingresso = serializers.CharField(read_only=True)
    forma_ingresso_display = serializers.SerializerMethodField()
    previsao_conclusao = serializers.IntegerField(read_only=True)
    aluno_especial = serializers.BooleanField(read_only=True)
    turno = serializers.CharField(read_only=True)
    turno_display = serializers.SerializerMethodField()
    
    # Status
    ativo = serializers.BooleanField(read_only=True)
    is_formado = serializers.BooleanField(read_only=True)
    situacao_academica = serializers.SerializerMethodField()
    
    # Dados de conclusão
    ano_conclusao = serializers.IntegerField(read_only=True, allow_null=True)
    data_colacao = serializers.DateField(read_only=True, allow_null=True)
    data_expedicao_diploma = serializers.DateField(read_only=True, allow_null=True)
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Dados do usuário base
    usuario = UsuarioCompletoAlunoSerializer(read_only=True)

    def get_forma_ingresso_display(self, obj):
        """Retorna a descrição legível da forma de ingresso."""
        return obj.get_forma_ingresso_display()

    def get_turno_display(self, obj):
        """Retorna a descrição legível do turno."""
        return obj.get_turno_display()

    def get_situacao_academica(self, obj):
        """Retorna a situação acadêmica atual do aluno."""
        if obj.is_formado:
            return 'Formado'
        if not obj.ativo:
            return 'Inativo'
        if obj.aluno_especial:
            return 'Aluno Especial'
        return 'Regular'


class AlunoResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de aluno para uso em nested serializers.
    
    Contém informações essenciais para identificação.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    ira = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    turno_display = serializers.SerializerMethodField()
    is_formado = serializers.BooleanField(read_only=True)

    def get_turno_display(self, obj):
        """Retorna a descrição legível do turno."""
        return obj.get_turno_display()


# ============================================================================
# SERIALIZERS PARA CONSULTAS ESPECÍFICAS
# ============================================================================

class AlunoFormadoSerializer(serializers.Serializer):
    """
    Serializer para alunos formados com dados de conclusão.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    cpf = serializers.CharField(source='usuario.cpf', read_only=True)
    ira = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    forma_ingresso_display = serializers.SerializerMethodField()
    ano_conclusao = serializers.IntegerField(read_only=True)
    data_colacao = serializers.DateField(read_only=True, allow_null=True)
    data_expedicao_diploma = serializers.DateField(read_only=True, allow_null=True)
    diploma_expedido = serializers.SerializerMethodField()

    def get_forma_ingresso_display(self, obj):
        """Retorna a descrição legível da forma de ingresso."""
        return obj.get_forma_ingresso_display()

    def get_diploma_expedido(self, obj):
        """Verifica se o diploma foi expedido."""
        return obj.data_expedicao_diploma is not None


class AlunoPorTurnoSerializer(serializers.Serializer):
    """
    Serializer para estatísticas de alunos por turno.
    """
    turno = serializers.CharField(read_only=True)
    turno_display = serializers.CharField(read_only=True)
    quantidade = serializers.IntegerField(read_only=True)


class AlunoPorFormaIngressoSerializer(serializers.Serializer):
    """
    Serializer para estatísticas de alunos por forma de ingresso.
    """
    forma_ingresso = serializers.CharField(read_only=True)
    forma_ingresso_display = serializers.CharField(read_only=True)
    quantidade = serializers.IntegerField(read_only=True)


class EstatisticasAlunosSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de alunos.
    """
    total_alunos = serializers.IntegerField(read_only=True)
    total_ativos = serializers.IntegerField(read_only=True)
    total_formados = serializers.IntegerField(read_only=True)
    total_especiais = serializers.IntegerField(read_only=True)
    media_ira = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    por_turno = AlunoPorTurnoSerializer(many=True, read_only=True)
    por_forma_ingresso = AlunoPorFormaIngressoSerializer(many=True, read_only=True)


# ============================================================================
# SERIALIZERS DE INPUT (Criação/Edição)
# ============================================================================

class AlunoCriarSerializer(serializers.Serializer):
    """
    Serializer para criação de um novo aluno.
    
    **Campos obrigatórios:**
    - usuario_id: ID do usuário base
    - previsao_conclusao: Ano previsto para conclusão do curso
    
    **Campos opcionais:**
    - ira: Índice de Rendimento Acadêmico (padrão: 0.00)
    - forma_ingresso: Forma de ingresso (padrão: ENEM)
    - aluno_especial: Se é aluno especial (padrão: False)
    - turno: Turno do aluno (padrão: Integral)
    - ativo: Se o aluno está ativo (padrão: True)
    """
    usuario_id = serializers.IntegerField(
        help_text='ID do usuário base'
    )
    ira = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.00,
        required=False,
        help_text='Índice de Rendimento Acadêmico (0.00 a 10.00)'
    )
    forma_ingresso = serializers.ChoiceField(
        choices=choices.FORMA_INGRESSO_OPCOES,
        default=choices.FORMA_INGRESSO_ENEM,
        required=False,
        help_text='Forma de ingresso do aluno'
    )
    previsao_conclusao = serializers.IntegerField(
        help_text='Ano previsto para conclusão do curso'
    )
    aluno_especial = serializers.BooleanField(
        default=False,
        required=False,
        help_text='Se o aluno é aluno especial'
    )
    turno = serializers.ChoiceField(
        choices=choices.TURNO_OPCOES,
        default=choices.TURNO_INTEGRAL,
        required=False,
        help_text='Turno do aluno'
    )
    ativo = serializers.BooleanField(
        default=True,
        required=False,
        help_text='Se o aluno está ativo'
    )

    def validate_usuario_id(self, value):
        """Valida se o usuário existe e se não é já um aluno."""
        from Usuarios.usuario.models import Usuario
        from Perfis.aluno.models import Aluno
        
        try:
            usuario = Usuario.objects.get(pk=value)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Usuário não encontrado.')
        
        if Aluno.objects.filter(usuario_id=value).exists():
            raise serializers.ValidationError('Este usuário já possui um perfil de aluno.')
        
        return value

    def validate_ira(self, value):
        """Valida se o IRA está entre 0 e 10."""
        if value < 0 or value > 10:
            raise serializers.ValidationError('O IRA deve estar entre 0.00 e 10.00.')
        return value


class AlunoEditarSerializer(serializers.Serializer):
    """
    Serializer para edição de um aluno existente.
    
    **Campos opcionais:**
    - ira: Índice de Rendimento Acadêmico
    - forma_ingresso: Forma de ingresso
    - previsao_conclusao: Ano previsto para conclusão
    - aluno_especial: Se é aluno especial
    - turno: Turno do aluno
    - ativo: Se o aluno está ativo
    - ano_conclusao: Ano de conclusão (para formados)
    - data_colacao: Data de colação (para formados)
    - data_expedicao_diploma: Data de expedição do diploma (para formados)
    """
    ira = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        required=False,
        help_text='Índice de Rendimento Acadêmico (0.00 a 10.00)'
    )
    forma_ingresso = serializers.ChoiceField(
        choices=choices.FORMA_INGRESSO_OPCOES,
        required=False,
        help_text='Forma de ingresso do aluno'
    )
    previsao_conclusao = serializers.IntegerField(
        required=False,
        help_text='Ano previsto para conclusão do curso'
    )
    aluno_especial = serializers.BooleanField(
        required=False,
        help_text='Se o aluno é aluno especial'
    )
    turno = serializers.ChoiceField(
        choices=choices.TURNO_OPCOES,
        required=False,
        help_text='Turno do aluno'
    )
    ativo = serializers.BooleanField(
        required=False,
        help_text='Se o aluno está ativo'
    )
    ano_conclusao = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text='Ano de conclusão do curso'
    )
    data_colacao = serializers.DateField(
        required=False,
        allow_null=True,
        help_text='Data de colação de grau'
    )
    data_expedicao_diploma = serializers.DateField(
        required=False,
        allow_null=True,
        help_text='Data de expedição do diploma'
    )

    def validate_ira(self, value):
        """Valida se o IRA está entre 0 e 10."""
        if value is not None and (value < 0 or value > 10):
            raise serializers.ValidationError('O IRA deve estar entre 0.00 e 10.00.')
        return value
