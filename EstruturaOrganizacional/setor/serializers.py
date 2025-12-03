from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from Usuarios.usuario.serializers import UsuarioReferenciaSerializer


# ============================================================================
# SERIALIZERS DE SETOR
# ============================================================================

class SetorListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de setores (versão resumida).
    
    Ideal para endpoints de listagem e seletores.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    sigla = serializers.CharField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    total_membros = serializers.SerializerMethodField()

    @extend_schema_field(serializers.IntegerField())
    def get_total_membros(self, obj) -> int:
        """Retorna o total de membros ativos no setor."""
        return obj.usuario_setores.filter(data_saida__isnull=True).count()


class SetorDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um setor.
    
    Inclui:
    - Dados do setor
    - Atividades associadas
    - Estatísticas de membros
    - Timestamps
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    sigla = serializers.CharField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    
    # Atividades
    atividades = serializers.SerializerMethodField()
    total_atividades = serializers.SerializerMethodField()
    
    # Estatísticas de membros
    total_membros = serializers.SerializerMethodField()
    total_responsaveis = serializers.SerializerMethodField()
    total_monitores = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_atividades(self, obj):
        """Retorna as atividades do setor."""
        from EstruturaOrganizacional.atividade.serializers import AtividadeResumoSerializer
        return AtividadeResumoSerializer(obj.atividades.all(), many=True).data

    def get_total_atividades(self, obj):
        """Retorna o total de atividades do setor."""
        return obj.atividades.count()

    def get_total_membros(self, obj):
        """Retorna o total de membros ativos no setor."""
        return obj.usuario_setores.filter(data_saida__isnull=True).count()

    def get_total_responsaveis(self, obj):
        """Retorna o total de responsáveis ativos no setor."""
        return obj.usuario_setores.filter(
            e_responsavel=True,
            data_saida__isnull=True
        ).count()

    def get_total_monitores(self, obj):
        """Retorna o total de monitores ativos no setor."""
        return obj.usuario_setores.filter(
            monitor=True,
            data_saida__isnull=True
        ).count()


class SetorResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de setor para uso em nested serializers.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    sigla = serializers.CharField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)


class SetorComMembrosSerializer(serializers.Serializer):
    """
    Serializer para visualizar setor com todos os seus membros.
    
    Agrupa os membros por função (responsável, monitor, membro comum).
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    sigla = serializers.CharField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    
    # Membros agrupados
    responsaveis = serializers.SerializerMethodField()
    monitores = serializers.SerializerMethodField()
    membros = serializers.SerializerMethodField()
    
    # Estatísticas
    total_membros_ativos = serializers.SerializerMethodField()

    def get_responsaveis(self, obj):
        """Retorna os responsáveis ativos do setor."""
        responsaveis = obj.usuario_setores.filter(
            e_responsavel=True,
            data_saida__isnull=True
        ).select_related('usuario')
        
        return [
            {
                'id': us.id,
                'usuario': UsuarioReferenciaSerializer(us.usuario).data,
                'data_entrada': us.data_entrada,
            }
            for us in responsaveis
        ]

    def get_monitores(self, obj):
        """Retorna os monitores ativos do setor."""
        monitores = obj.usuario_setores.filter(
            monitor=True,
            e_responsavel=False,
            data_saida__isnull=True
        ).select_related('usuario')
        
        return [
            {
                'id': us.id,
                'usuario': UsuarioReferenciaSerializer(us.usuario).data,
                'data_entrada': us.data_entrada,
            }
            for us in monitores
        ]

    def get_membros(self, obj):
        """Retorna os membros comuns ativos do setor."""
        membros = obj.usuario_setores.filter(
            e_responsavel=False,
            monitor=False,
            data_saida__isnull=True
        ).select_related('usuario')
        
        return [
            {
                'id': us.id,
                'usuario': UsuarioReferenciaSerializer(us.usuario).data,
                'data_entrada': us.data_entrada,
            }
            for us in membros
        ]

    def get_total_membros_ativos(self, obj):
        """Retorna o total de membros ativos."""
        return obj.usuario_setores.filter(data_saida__isnull=True).count()


class SetorComAtividadesSerializer(serializers.Serializer):
    """
    Serializer para visualizar setor com suas atividades e funções.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    sigla = serializers.CharField(read_only=True, allow_null=True)
    is_active = serializers.BooleanField(read_only=True)
    
    # Atividades com funções
    atividades = serializers.SerializerMethodField()
    total_atividades = serializers.SerializerMethodField()
    total_funcoes = serializers.SerializerMethodField()

    def get_atividades(self, obj):
        """Retorna as atividades com suas funções."""
        from EstruturaOrganizacional.atividade.serializers import AtividadeComFuncoesSerializer
        return AtividadeComFuncoesSerializer(obj.atividades.all(), many=True).data

    def get_total_atividades(self, obj):
        """Retorna o total de atividades."""
        return obj.atividades.count()

    def get_total_funcoes(self, obj):
        """Retorna o total de funções em todas as atividades."""
        total = 0
        for atividade in obj.atividades.all():
            total += atividade.funcoes.count()
        return total


# ============================================================================
# SERIALIZERS PARA ESTATÍSTICAS
# ============================================================================

class EstatisticasSetoresSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de setores.
    """
    total_setores = serializers.IntegerField(read_only=True)
    total_ativos = serializers.IntegerField(read_only=True)
    total_inativos = serializers.IntegerField(read_only=True)
    total_membros_vinculados = serializers.IntegerField(read_only=True)
    setores_por_tamanho = serializers.ListField(read_only=True)


# ============================================================================
# SERIALIZERS DE INPUT (Criação/Edição)
# ============================================================================

class SetorCriarSerializer(serializers.Serializer):
    """
    Serializer para criação de um novo setor.
    
    **Campos obrigatórios:**
    - nome: Nome do setor
    
    **Campos opcionais:**
    - sigla: Sigla do setor
    - is_active: Se o setor está ativo (padrão: True)
    """
    nome = serializers.CharField(
        max_length=255,
        help_text='Nome do setor'
    )
    sigla = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='Sigla do setor'
    )
    is_active = serializers.BooleanField(
        default=True,
        required=False,
        help_text='Se o setor está ativo'
    )


class SetorEditarSerializer(serializers.Serializer):
    """
    Serializer para edição de um setor existente.
    
    **Campos opcionais:**
    - nome: Nome do setor
    - sigla: Sigla do setor
    - is_active: Se o setor está ativo
    """
    nome = serializers.CharField(
        max_length=255,
        required=False,
        help_text='Nome do setor'
    )
    sigla = serializers.CharField(
        max_length=50,
        required=False,
        allow_blank=True,
        allow_null=True,
        help_text='Sigla do setor'
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text='Se o setor está ativo'
    )
