from rest_framework import serializers


# ============================================================================
# SERIALIZERS DE CURSO
# ============================================================================

class CursoListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de cursos (versão resumida).
    
    Ideal para endpoints de listagem e seletores.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    descricao = serializers.CharField(read_only=True, allow_null=True)
    descricao_resumida = serializers.SerializerMethodField()
    total_estagiarios = serializers.SerializerMethodField()

    def get_descricao_resumida(self, obj):
        """Retorna a descrição resumida."""
        if obj.descricao and len(obj.descricao) > 100:
            return f'{obj.descricao[:100]}...'
        return obj.descricao

    def get_total_estagiarios(self, obj):
        """Retorna o total de estagiários do curso."""
        return obj.estagiarios.count()


class CursoDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um curso.
    
    Inclui:
    - Dados do curso
    - Estatísticas de estagiários
    - Timestamps
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    descricao = serializers.CharField(read_only=True, allow_null=True)
    
    # Estatísticas de estagiários
    total_estagiarios = serializers.SerializerMethodField()
    estagiarios_estagios_ativos = serializers.SerializerMethodField()
    media_carga_horaria = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_total_estagiarios(self, obj):
        """Retorna o total de estagiários do curso."""
        return obj.estagiarios.count()

    def get_estagiarios_estagios_ativos(self, obj):
        """Retorna o total de estagiários com estágio ativo."""
        from django.utils import timezone
        from django.db.models import Q
        
        hoje = timezone.now().date()
        return obj.estagiarios.filter(
            Q(data_fim_estagio__isnull=True) | Q(data_fim_estagio__gte=hoje)
        ).count()

    def get_media_carga_horaria(self, obj):
        """Retorna a média de carga horária dos estagiários."""
        from django.db.models import Avg
        
        media = obj.estagiarios.aggregate(media=Avg('carga_horaria'))['media']
        return round(media, 2) if media else 0


class CursoResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de curso para uso em nested serializers.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)


class CursoComEstagiariosSerializer(serializers.Serializer):
    """
    Serializer para visualizar curso com seus estagiários.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    descricao = serializers.CharField(read_only=True, allow_null=True)
    
    # Estagiários
    estagiarios = serializers.SerializerMethodField()
    
    # Estatísticas
    estatisticas = serializers.SerializerMethodField()

    def get_estagiarios(self, obj):
        """Retorna os estagiários do curso."""
        from django.utils import timezone
        
        hoje = timezone.now().date()
        estagiarios = obj.estagiarios.select_related('usuario', 'empresa').all()
        
        return [
            {
                'usuario_id': e.usuario.id,
                'nome': e.usuario.nome,
                'cpf': e.usuario.cpf,
                'empresa': {
                    'id': e.empresa.id,
                    'nome': e.empresa.nome,
                },
                'carga_horaria': e.carga_horaria,
                'data_inicio_estagio': e.data_inicio_estagio,
                'data_fim_estagio': e.data_fim_estagio,
                'estagio_ativo': e.data_fim_estagio is None or e.data_fim_estagio >= hoje,
            }
            for e in estagiarios
        ]

    def get_estatisticas(self, obj):
        """Retorna estatísticas do curso."""
        from django.utils import timezone
        from django.db.models import Q, Avg
        
        hoje = timezone.now().date()
        
        total = obj.estagiarios.count()
        ativos = obj.estagiarios.filter(
            Q(data_fim_estagio__isnull=True) | Q(data_fim_estagio__gte=hoje)
        ).count()
        media_carga = obj.estagiarios.aggregate(media=Avg('carga_horaria'))['media']
        
        return {
            'total_estagiarios': total,
            'estagios_ativos': ativos,
            'estagios_encerrados': total - ativos,
            'media_carga_horaria': round(media_carga, 2) if media_carga else 0,
        }


# ============================================================================
# SERIALIZERS PARA ESTATÍSTICAS
# ============================================================================

class EstatisticasCursosSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de cursos.
    """
    total_cursos = serializers.IntegerField(read_only=True)
    total_estagiarios = serializers.IntegerField(read_only=True)
    media_estagiarios_por_curso = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        read_only=True
    )
    cursos_por_quantidade_estagiarios = serializers.ListField(read_only=True)


class CursoPorQuantidadeEstagiariosSerializer(serializers.Serializer):
    """
    Serializer para ranking de cursos por quantidade de estagiários.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    total_estagiarios = serializers.IntegerField(read_only=True)
    estagios_ativos = serializers.IntegerField(read_only=True)
