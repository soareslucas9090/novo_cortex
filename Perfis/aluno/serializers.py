from rest_framework import serializers

from Usuarios.usuario.serializers import (
    CampusResumoSerializer,
    ContatoListaSerializer,
    EnderecoListaSerializer,
    UsuarioSetorResumoSerializer,
)


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
    is_active = serializers.BooleanField(read_only=True)
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
    is_active = serializers.BooleanField(read_only=True)
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
    is_active = serializers.BooleanField(read_only=True)
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
        if not obj.is_active:
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
