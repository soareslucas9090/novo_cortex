from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from EstruturaOrganizacional.atividade.serializers import AtividadeResumoSerializer


# ============================================================================
# SERIALIZERS DE FUNÇÃO
# ============================================================================

class FuncaoListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de funções (versão resumida).
    
    Ideal para endpoints de listagem.
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    descricao_resumida = serializers.SerializerMethodField()
    atividade = AtividadeResumoSerializer(read_only=True)
    setor_nome = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_descricao_resumida(self, obj) -> str:
        """Retorna a descrição resumida (primeiros 100 caracteres)."""
        if len(obj.descricao) > 100:
            return f'{obj.descricao[:100]}...'
        return obj.descricao

    @extend_schema_field(serializers.CharField())
    def get_setor_nome(self, obj) -> str:
        """Retorna o nome do setor da atividade."""
        return obj.atividade.setor.nome


class FuncaoDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de uma função.
    
    Inclui:
    - Dados da função
    - Atividade associada
    - Setor (via atividade)
    - Timestamps
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    
    # Atividade
    atividade = AtividadeResumoSerializer(read_only=True)
    
    # Setor (via atividade)
    setor = serializers.SerializerMethodField()
    
    # Hierarquia completa
    hierarquia = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_setor(self, obj):
        """Retorna os dados do setor."""
        from EstruturaOrganizacional.setor.serializers import SetorResumoSerializer
        return SetorResumoSerializer(obj.atividade.setor).data

    def get_hierarquia(self, obj):
        """Retorna a hierarquia completa: Setor > Atividade > Função."""
        return {
            'setor': obj.atividade.setor.nome,
            'atividade': obj.atividade.descricao[:50] if len(obj.atividade.descricao) > 50 else obj.atividade.descricao,
            'funcao': obj.descricao[:50] if len(obj.descricao) > 50 else obj.descricao,
        }


class FuncaoResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de função para uso em nested serializers.
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


# ============================================================================
# SERIALIZERS PARA CONSULTAS ESPECÍFICAS
# ============================================================================

class FuncaoPorAtividadeSerializer(serializers.Serializer):
    """
    Serializer para listar funções de uma atividade específica.
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)


class FuncaoPorSetorSerializer(serializers.Serializer):
    """
    Serializer para listar funções de um setor (via atividades).
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    atividade_descricao = serializers.CharField(source='atividade.descricao', read_only=True)


class HierarquiaSetorSerializer(serializers.Serializer):
    """
    Serializer para visualizar a hierarquia completa de um setor.
    
    Estrutura: Setor > Atividades > Funções
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    # Hierarquia
    atividades = serializers.SerializerMethodField()
    
    # Estatísticas
    total_atividades = serializers.SerializerMethodField()
    total_funcoes = serializers.SerializerMethodField()

    def get_atividades(self, obj):
        """Retorna as atividades com suas funções."""
        atividades_data = []
        for atividade in obj.atividades.all():
            atividade_item = {
                'id': atividade.id,
                'descricao': atividade.descricao,
                'funcoes': [
                    {
                        'id': funcao.id,
                        'descricao': funcao.descricao,
                    }
                    for funcao in atividade.funcoes.all()
                ],
                'total_funcoes': atividade.funcoes.count(),
            }
            atividades_data.append(atividade_item)
        return atividades_data

    def get_total_atividades(self, obj):
        """Retorna o total de atividades."""
        return obj.atividades.count()

    def get_total_funcoes(self, obj):
        """Retorna o total de funções."""
        total = 0
        for atividade in obj.atividades.all():
            total += atividade.funcoes.count()
        return total


class EstatisticasFuncoesSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de funções.
    """
    total_funcoes = serializers.IntegerField(read_only=True)
    funcoes_por_atividade = serializers.ListField(read_only=True)
    funcoes_por_setor = serializers.ListField(read_only=True)


# ============================================================================
# SERIALIZERS DE INPUT (Criação/Edição)
# ============================================================================

class FuncaoCriarSerializer(serializers.Serializer):
    """
    Serializer para criação de uma nova função.
    
    **Campos obrigatórios:**
    - atividade_id: ID da atividade à qual a função pertence
    - descricao: Descrição da função
    """
    atividade_id = serializers.IntegerField(
        help_text='ID da atividade à qual a função pertence'
    )
    descricao = serializers.CharField(
        help_text='Descrição da função'
    )

    def validate_atividade_id(self, value):
        """Valida se a atividade existe."""
        from EstruturaOrganizacional.atividade.models import Atividade
        try:
            atividade = Atividade.objects.get(id=value)
        except Atividade.DoesNotExist:
            raise serializers.ValidationError('Atividade não encontrada.')
        return atividade

    def validate(self, attrs):
        """Renomeia atividade_id para atividade."""
        attrs['atividade'] = attrs.pop('atividade_id')
        return attrs


class FuncaoEditarSerializer(serializers.Serializer):
    """
    Serializer para edição de uma função existente.
    
    **Campos opcionais:**
    - atividade_id: ID da atividade à qual a função pertence
    - descricao: Descrição da função
    """
    atividade_id = serializers.IntegerField(
        required=False,
        help_text='ID da atividade à qual a função pertence'
    )
    descricao = serializers.CharField(
        required=False,
        help_text='Descrição da função'
    )

    def validate_atividade_id(self, value):
        """Valida se a atividade existe."""
        from EstruturaOrganizacional.atividade.models import Atividade
        try:
            atividade = Atividade.objects.get(id=value)
        except Atividade.DoesNotExist:
            raise serializers.ValidationError('Atividade não encontrada.')
        return atividade

    def validate(self, attrs):
        """Renomeia atividade_id para atividade se existir."""
        if 'atividade_id' in attrs:
            attrs['atividade'] = attrs.pop('atividade_id')
        return attrs
