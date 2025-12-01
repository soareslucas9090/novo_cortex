from rest_framework import serializers

from Usuarios.usuario.serializers import (
    CampusResumoSerializer,
    UsuarioReferenciaSerializer,
    UsuarioResumoSerializer,
)


# ============================================================================
# SERIALIZERS DE MATRÍCULA
# ============================================================================

class MatriculaListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de matrículas (versão resumida).
    
    Ideal para endpoints de listagem onde não é necessário
    carregar todos os dados do usuário.
    """
    # Identificação
    matricula = serializers.CharField(read_only=True)
    
    # Dados do usuário (resumido)
    usuario = UsuarioReferenciaSerializer(read_only=True)
    
    # Datas
    data_expedicao = serializers.DateField(read_only=True)
    data_validade = serializers.DateField(read_only=True)
    
    # Status
    is_active = serializers.BooleanField(read_only=True)
    esta_valida = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_esta_valida(self, obj):
        """Verifica se a matrícula está válida (ativa e não expirada)."""
        from django.utils import timezone
        
        if not obj.is_active:
            return False
        return obj.data_validade >= timezone.now().date()

    def get_status(self, obj):
        """Retorna o status da matrícula."""
        from django.utils import timezone
        
        if not obj.is_active:
            return 'Inativa'
        if obj.data_validade < timezone.now().date():
            return 'Expirada'
        return 'Válida'


class MatriculaDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de uma matrícula.
    
    Inclui:
    - Dados completos da matrícula
    - Informações resumidas do usuário
    - Métricas de validade
    """
    # Identificação
    matricula = serializers.CharField(read_only=True)
    
    # Dados do usuário
    usuario = UsuarioResumoSerializer(read_only=True)
    
    # Datas
    data_expedicao = serializers.DateField(read_only=True)
    data_validade = serializers.DateField(read_only=True)
    
    # Status
    is_active = serializers.BooleanField(read_only=True)
    esta_valida = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    
    # Métricas
    dias_ate_expiracao = serializers.SerializerMethodField()
    tempo_desde_expedicao_dias = serializers.SerializerMethodField()
    validade_em_dias = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_esta_valida(self, obj):
        """Verifica se a matrícula está válida (ativa e não expirada)."""
        from django.utils import timezone
        
        if not obj.is_active:
            return False
        return obj.data_validade >= timezone.now().date()

    def get_status(self, obj):
        """Retorna o status da matrícula."""
        from django.utils import timezone
        
        if not obj.is_active:
            return 'Inativa'
        if obj.data_validade < timezone.now().date():
            return 'Expirada'
        return 'Válida'

    def get_dias_ate_expiracao(self, obj):
        """Calcula os dias até a expiração (negativo se já expirou)."""
        from django.utils import timezone
        
        delta = obj.data_validade - timezone.now().date()
        return delta.days

    def get_tempo_desde_expedicao_dias(self, obj):
        """Calcula o tempo desde a expedição em dias."""
        from django.utils import timezone
        
        delta = timezone.now().date() - obj.data_expedicao
        return delta.days

    def get_validade_em_dias(self, obj):
        """Calcula o período total de validade em dias."""
        delta = obj.data_validade - obj.data_expedicao
        return delta.days


class MatriculaResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de matrícula para uso em nested serializers.
    
    Contém informações essenciais para identificação.
    """
    matricula = serializers.CharField(read_only=True)
    data_validade = serializers.DateField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    esta_valida = serializers.SerializerMethodField()

    def get_esta_valida(self, obj):
        """Verifica se a matrícula está válida."""
        from django.utils import timezone
        
        if not obj.is_active:
            return False
        return obj.data_validade >= timezone.now().date()


# ============================================================================
# SERIALIZERS PARA CONSULTAS ESPECÍFICAS
# ============================================================================

class MatriculaPorUsuarioSerializer(serializers.Serializer):
    """
    Serializer para listar matrículas de um usuário específico.
    
    Ideal para endpoints que retornam o histórico de matrículas.
    """
    matricula = serializers.CharField(read_only=True)
    data_expedicao = serializers.DateField(read_only=True)
    data_validade = serializers.DateField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    esta_valida = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    dias_ate_expiracao = serializers.SerializerMethodField()

    def get_esta_valida(self, obj):
        """Verifica se a matrícula está válida."""
        from django.utils import timezone
        
        if not obj.is_active:
            return False
        return obj.data_validade >= timezone.now().date()

    def get_status(self, obj):
        """Retorna o status da matrícula."""
        from django.utils import timezone
        
        if not obj.is_active:
            return 'Inativa'
        if obj.data_validade < timezone.now().date():
            return 'Expirada'
        return 'Válida'

    def get_dias_ate_expiracao(self, obj):
        """Calcula os dias até a expiração."""
        from django.utils import timezone
        
        delta = obj.data_validade - timezone.now().date()
        return delta.days


class UsuarioComMatriculasSerializer(serializers.Serializer):
    """
    Serializer para visualizar usuário com suas matrículas.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cpf = serializers.CharField(read_only=True)
    cpf_formatado = serializers.SerializerMethodField()
    campus = CampusResumoSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    
    # Matrículas
    matriculas = MatriculaPorUsuarioSerializer(many=True, read_only=True)
    matricula_ativa = serializers.SerializerMethodField()
    total_matriculas = serializers.SerializerMethodField()

    def get_cpf_formatado(self, obj):
        """Retorna o CPF formatado (XXX.XXX.XXX-XX)."""
        cpf = obj.cpf
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf

    def get_matricula_ativa(self, obj):
        """Retorna a matrícula ativa atual (se houver)."""
        from django.utils import timezone
        
        hoje = timezone.now().date()
        matricula_ativa = obj.matriculas.filter(
            is_active=True,
            data_validade__gte=hoje
        ).first()
        
        if matricula_ativa:
            return MatriculaResumoSerializer(matricula_ativa).data
        return None

    def get_total_matriculas(self, obj):
        """Retorna o total de matrículas do usuário."""
        return obj.matriculas.count()


class MatriculasExpirandoSerializer(serializers.Serializer):
    """
    Serializer para matrículas próximas da expiração.
    
    Ideal para alertas e relatórios.
    """
    matricula = serializers.CharField(read_only=True)
    usuario = UsuarioReferenciaSerializer(read_only=True)
    data_validade = serializers.DateField(read_only=True)
    dias_ate_expiracao = serializers.SerializerMethodField()
    urgencia = serializers.SerializerMethodField()

    def get_dias_ate_expiracao(self, obj):
        """Calcula os dias até a expiração."""
        from django.utils import timezone
        
        delta = obj.data_validade - timezone.now().date()
        return delta.days

    def get_urgencia(self, obj):
        """Retorna o nível de urgência baseado nos dias restantes."""
        from django.utils import timezone
        
        dias = (obj.data_validade - timezone.now().date()).days
        
        if dias <= 0:
            return 'Expirada'
        elif dias <= 7:
            return 'Crítica'
        elif dias <= 30:
            return 'Alta'
        elif dias <= 60:
            return 'Média'
        else:
            return 'Baixa'


class MatriculasExpiradasSerializer(serializers.Serializer):
    """
    Serializer para matrículas já expiradas.
    """
    matricula = serializers.CharField(read_only=True)
    usuario = UsuarioReferenciaSerializer(read_only=True)
    data_validade = serializers.DateField(read_only=True)
    dias_desde_expiracao = serializers.SerializerMethodField()

    def get_dias_desde_expiracao(self, obj):
        """Calcula os dias desde a expiração."""
        from django.utils import timezone
        
        delta = timezone.now().date() - obj.data_validade
        return delta.days


class EstatisticasMatriculasSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de matrículas.
    """
    total_matriculas = serializers.IntegerField(read_only=True)
    total_ativas = serializers.IntegerField(read_only=True)
    total_inativas = serializers.IntegerField(read_only=True)
    total_validas = serializers.IntegerField(read_only=True)
    total_expiradas = serializers.IntegerField(read_only=True)
    expirando_proximos_7_dias = serializers.IntegerField(read_only=True)
    expirando_proximos_30_dias = serializers.IntegerField(read_only=True)
    expirando_proximos_60_dias = serializers.IntegerField(read_only=True)
