from rest_framework import serializers

from Usuarios.usuario.serializers import (
    CampusResumoSerializer,
    SetorResumoSerializer,
    UsuarioReferenciaSerializer,
    UsuarioResumoSerializer,
)


# ============================================================================
# SERIALIZERS DE USUARIO_SETOR
# ============================================================================

class UsuarioSetorListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de vínculos usuario-setor (versão resumida).
    
    Ideal para endpoints de listagem onde não é necessário
    carregar todos os dados relacionados.
    """
    id = serializers.IntegerField(read_only=True)
    usuario = UsuarioReferenciaSerializer(read_only=True)
    setor = SetorResumoSerializer(read_only=True)
    campus = CampusResumoSerializer(read_only=True)
    e_responsavel = serializers.BooleanField(read_only=True)
    monitor = serializers.BooleanField(read_only=True)
    vinculo_ativo = serializers.SerializerMethodField()

    def get_vinculo_ativo(self, obj):
        """Verifica se o vínculo com o setor está ativo."""
        return obj.data_saida is None


class UsuarioSetorDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um vínculo usuario-setor.
    
    Inclui:
    - Dados do vínculo
    - Informações completas do usuário (resumidas)
    - Informações do setor
    - Informações do campus
    - Datas de entrada e saída
    - Status do vínculo
    """
    id = serializers.IntegerField(read_only=True)
    
    # Relacionamentos
    usuario = UsuarioResumoSerializer(read_only=True)
    setor = SetorResumoSerializer(read_only=True)
    campus = CampusResumoSerializer(read_only=True)
    
    # Dados do vínculo
    e_responsavel = serializers.BooleanField(read_only=True)
    monitor = serializers.BooleanField(read_only=True)
    data_entrada = serializers.DateField(read_only=True)
    data_saida = serializers.DateField(read_only=True, allow_null=True)
    
    # Status
    vinculo_ativo = serializers.SerializerMethodField()
    tempo_vinculo = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_vinculo_ativo(self, obj):
        """Verifica se o vínculo com o setor está ativo."""
        return obj.data_saida is None

    def get_tempo_vinculo(self, obj):
        """Retorna o tempo de vínculo em dias."""
        from django.utils import timezone
        
        data_fim = obj.data_saida if obj.data_saida else timezone.now().date()
        delta = data_fim - obj.data_entrada
        return delta.days


# ============================================================================
# SERIALIZERS PARA CONSULTAS ESPECÍFICAS
# ============================================================================

class UsuarioSetorPorSetorSerializer(serializers.Serializer):
    """
    Serializer para listar usuários de um setor específico.
    
    Ideal para endpoints que retornam todos os membros de um setor.
    """
    id = serializers.IntegerField(read_only=True)
    usuario = UsuarioResumoSerializer(read_only=True)
    e_responsavel = serializers.BooleanField(read_only=True)
    monitor = serializers.BooleanField(read_only=True)
    data_entrada = serializers.DateField(read_only=True)
    data_saida = serializers.DateField(read_only=True, allow_null=True)
    vinculo_ativo = serializers.SerializerMethodField()

    def get_vinculo_ativo(self, obj):
        """Verifica se o vínculo está ativo."""
        return obj.data_saida is None


class UsuarioSetorPorUsuarioSerializer(serializers.Serializer):
    """
    Serializer para listar setores de um usuário específico.
    
    Ideal para endpoints que retornam todos os setores de um usuário.
    """
    id = serializers.IntegerField(read_only=True)
    setor = SetorResumoSerializer(read_only=True)
    campus = CampusResumoSerializer(read_only=True)
    e_responsavel = serializers.BooleanField(read_only=True)
    monitor = serializers.BooleanField(read_only=True)
    data_entrada = serializers.DateField(read_only=True)
    data_saida = serializers.DateField(read_only=True, allow_null=True)
    vinculo_ativo = serializers.SerializerMethodField()
    tempo_vinculo = serializers.SerializerMethodField()

    def get_vinculo_ativo(self, obj):
        """Verifica se o vínculo está ativo."""
        return obj.data_saida is None

    def get_tempo_vinculo(self, obj):
        """Retorna o tempo de vínculo em dias."""
        from django.utils import timezone
        
        data_fim = obj.data_saida if obj.data_saida else timezone.now().date()
        delta = data_fim - obj.data_entrada
        return delta.days


class SetorComUsuariosSerializer(serializers.Serializer):
    """
    Serializer para visualizar um setor com todos os seus usuários.
    
    Agrupa os usuários por tipo (responsável, monitor, membros).
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    ativo = serializers.BooleanField(read_only=True)
    
    # Usuários agrupados
    responsaveis = serializers.SerializerMethodField()
    monitores = serializers.SerializerMethodField()
    membros = serializers.SerializerMethodField()
    total_membros_ativos = serializers.SerializerMethodField()

    def get_responsaveis(self, obj):
        """Retorna os responsáveis do setor."""
        responsaveis = obj.usuario_setores.filter(
            e_responsavel=True,
            data_saida__isnull=True
        ).select_related('usuario', 'usuario__campus')
        return [
            {
                'id': us.id,
                'usuario': UsuarioReferenciaSerializer(us.usuario).data,
                'data_entrada': us.data_entrada,
            }
            for us in responsaveis
        ]

    def get_monitores(self, obj):
        """Retorna os monitores do setor."""
        monitores = obj.usuario_setores.filter(
            monitor=True,
            data_saida__isnull=True
        ).select_related('usuario', 'usuario__campus')
        return [
            {
                'id': us.id,
                'usuario': UsuarioReferenciaSerializer(us.usuario).data,
                'data_entrada': us.data_entrada,
            }
            for us in monitores
        ]

    def get_membros(self, obj):
        """Retorna os membros comuns do setor (não responsáveis nem monitores)."""
        membros = obj.usuario_setores.filter(
            e_responsavel=False,
            monitor=False,
            data_saida__isnull=True
        ).select_related('usuario', 'usuario__campus')
        return [
            {
                'id': us.id,
                'usuario': UsuarioReferenciaSerializer(us.usuario).data,
                'data_entrada': us.data_entrada,
            }
            for us in membros
        ]

    def get_total_membros_ativos(self, obj):
        """Retorna o total de membros ativos no setor."""
        return obj.usuario_setores.filter(data_saida__isnull=True).count()
