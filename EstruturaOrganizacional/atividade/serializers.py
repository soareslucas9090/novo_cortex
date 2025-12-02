from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from EstruturaOrganizacional.setor.serializers import SetorResumoSerializer


# ============================================================================
# SERIALIZERS DE ATIVIDADE
# ============================================================================

class AtividadeListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de atividades (versão resumida).
    
    Ideal para endpoints de listagem.
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    descricao_resumida = serializers.SerializerMethodField()
    setor = SetorResumoSerializer(read_only=True)
    total_funcoes = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_descricao_resumida(self, obj) -> str:
        """Retorna a descrição resumida (primeiros 100 caracteres)."""
        if len(obj.descricao) > 100:
            return f'{obj.descricao[:100]}...'
        return obj.descricao

    @extend_schema_field(serializers.IntegerField())
    def get_total_funcoes(self, obj) -> int:
        """Retorna o total de funções da atividade."""
        return obj.funcoes.count()


class AtividadeDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de uma atividade.
    
    Inclui:
    - Dados da atividade
    - Setor associado
    - Funções associadas
    - Timestamps
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    setor = SetorResumoSerializer(read_only=True)
    
    # Funções
    funcoes = serializers.SerializerMethodField()
    total_funcoes = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_funcoes(self, obj):
        """Retorna as funções da atividade."""
        from EstruturaOrganizacional.funcao.serializers import FuncaoResumoSerializer
        return FuncaoResumoSerializer(obj.funcoes.all(), many=True).data

    def get_total_funcoes(self, obj):
        """Retorna o total de funções."""
        return obj.funcoes.count()


class AtividadeResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de atividade para uso em nested serializers.
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    descricao_resumida = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_descricao_resumida(self, obj) -> str:
        """Retorna a descrição resumida."""
        if len(obj.descricao) > 50:
            return f'{obj.descricao[:50]}...'
        return obj.descricao


class AtividadeComFuncoesSerializer(serializers.Serializer):
    """
    Serializer para visualizar atividade com suas funções.
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    
    # Funções
    funcoes = serializers.SerializerMethodField()
    total_funcoes = serializers.SerializerMethodField()

    def get_funcoes(self, obj):
        """Retorna as funções da atividade."""
        from EstruturaOrganizacional.funcao.serializers import FuncaoResumoSerializer
        return FuncaoResumoSerializer(obj.funcoes.all(), many=True).data

    def get_total_funcoes(self, obj):
        """Retorna o total de funções."""
        return obj.funcoes.count()


# ============================================================================
# SERIALIZERS PARA CONSULTAS ESPECÍFICAS
# ============================================================================

class AtividadePorSetorSerializer(serializers.Serializer):
    """
    Serializer para listar atividades de um setor específico.
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    total_funcoes = serializers.SerializerMethodField()

    def get_total_funcoes(self, obj):
        """Retorna o total de funções."""
        return obj.funcoes.count()


class EstatisticasAtividadesSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de atividades.
    """
    total_atividades = serializers.IntegerField(read_only=True)
    total_funcoes = serializers.IntegerField(read_only=True)
    media_funcoes_por_atividade = serializers.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        read_only=True
    )
    atividades_por_setor = serializers.ListField(read_only=True)


# ============================================================================
# SERIALIZERS DE INPUT (Criação/Edição)
# ============================================================================

class AtividadeCriarSerializer(serializers.Serializer):
    """
    Serializer para criação de uma nova atividade.
    
    **Campos obrigatórios:**
    - setor_id: ID do setor ao qual a atividade pertence
    - descricao: Descrição da atividade
    """
    setor_id = serializers.IntegerField(
        help_text='ID do setor ao qual a atividade pertence'
    )
    descricao = serializers.CharField(
        help_text='Descrição da atividade'
    )

    def validate_setor_id(self, value):
        """Valida se o setor existe."""
        from EstruturaOrganizacional.setor.models import Setor
        try:
            setor = Setor.objects.get(id=value)
        except Setor.DoesNotExist:
            raise serializers.ValidationError('Setor não encontrado.')
        return setor

    def validate(self, attrs):
        """Renomeia setor_id para setor."""
        attrs['setor'] = attrs.pop('setor_id')
        return attrs


class AtividadeEditarSerializer(serializers.Serializer):
    """
    Serializer para edição de uma atividade existente.
    
    **Campos opcionais:**
    - setor_id: ID do setor ao qual a atividade pertence
    - descricao: Descrição da atividade
    """
    setor_id = serializers.IntegerField(
        required=False,
        help_text='ID do setor ao qual a atividade pertence'
    )
    descricao = serializers.CharField(
        required=False,
        help_text='Descrição da atividade'
    )

    def validate_setor_id(self, value):
        """Valida se o setor existe."""
        from EstruturaOrganizacional.setor.models import Setor
        try:
            setor = Setor.objects.get(id=value)
        except Setor.DoesNotExist:
            raise serializers.ValidationError('Setor não encontrado.')
        return setor

    def validate(self, attrs):
        """Renomeia setor_id para setor se existir."""
        if 'setor_id' in attrs:
            attrs['setor'] = attrs.pop('setor_id')
        return attrs
