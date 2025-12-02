from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


# ============================================================================
# SERIALIZERS DE EMPRESA
# ============================================================================

class EmpresaListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de empresas (versão resumida).
    
    Ideal para endpoints de listagem e seletores.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    cnpj_formatado = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    total_terceirizados = serializers.SerializerMethodField()
    total_estagiarios = serializers.SerializerMethodField()

    @extend_schema_field(serializers.CharField())
    def get_cnpj_formatado(self, obj) -> str:
        """Retorna o CNPJ formatado (XX.XXX.XXX/XXXX-XX)."""
        cnpj = obj.cnpj
        if len(cnpj) == 14:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        return cnpj

    @extend_schema_field(serializers.IntegerField())
    def get_total_terceirizados(self, obj) -> int:
        """Retorna o total de terceirizados da empresa."""
        return obj.terceirizados.count()

    @extend_schema_field(serializers.IntegerField())
    def get_total_estagiarios(self, obj) -> int:
        """Retorna o total de estagiários da empresa."""
        return obj.estagiarios.count()


class EmpresaDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de uma empresa.
    
    Inclui:
    - Dados da empresa
    - Estatísticas de terceirizados e estagiários
    - Contratos ativos
    - Timestamps
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    cnpj_formatado = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    
    # Estatísticas de terceirizados
    total_terceirizados = serializers.SerializerMethodField()
    terceirizados_contratos_ativos = serializers.SerializerMethodField()
    
    # Estatísticas de estagiários
    total_estagiarios = serializers.SerializerMethodField()
    estagiarios_estagios_ativos = serializers.SerializerMethodField()
    
    # Total geral
    total_vinculos = serializers.SerializerMethodField()
    total_vinculos_ativos = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_cnpj_formatado(self, obj):
        """Retorna o CNPJ formatado."""
        cnpj = obj.cnpj
        if len(cnpj) == 14:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        return cnpj

    def get_total_terceirizados(self, obj):
        """Retorna o total de terceirizados."""
        return obj.terceirizados.count()

    def get_terceirizados_contratos_ativos(self, obj):
        """Retorna o total de terceirizados com contrato ativo."""
        from django.utils import timezone
        from django.db.models import Q
        
        hoje = timezone.now().date()
        return obj.terceirizados.filter(
            Q(data_fim_contrato__isnull=True) | Q(data_fim_contrato__gte=hoje)
        ).count()

    def get_total_estagiarios(self, obj):
        """Retorna o total de estagiários."""
        return obj.estagiarios.count()

    def get_estagiarios_estagios_ativos(self, obj):
        """Retorna o total de estagiários com estágio ativo."""
        from django.utils import timezone
        from django.db.models import Q
        
        hoje = timezone.now().date()
        return obj.estagiarios.filter(
            Q(data_fim_estagio__isnull=True) | Q(data_fim_estagio__gte=hoje)
        ).count()

    def get_total_vinculos(self, obj):
        """Retorna o total de vínculos (terceirizados + estagiários)."""
        return obj.terceirizados.count() + obj.estagiarios.count()

    def get_total_vinculos_ativos(self, obj):
        """Retorna o total de vínculos ativos."""
        from django.utils import timezone
        from django.db.models import Q
        
        hoje = timezone.now().date()
        
        terceirizados_ativos = obj.terceirizados.filter(
            Q(data_fim_contrato__isnull=True) | Q(data_fim_contrato__gte=hoje)
        ).count()
        
        estagiarios_ativos = obj.estagiarios.filter(
            Q(data_fim_estagio__isnull=True) | Q(data_fim_estagio__gte=hoje)
        ).count()
        
        return terceirizados_ativos + estagiarios_ativos


class EmpresaResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de empresa para uso em nested serializers.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class EmpresaComVinculosSerializer(serializers.Serializer):
    """
    Serializer para visualizar empresa com seus terceirizados e estagiários.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    cnpj_formatado = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    
    # Terceirizados
    terceirizados = serializers.SerializerMethodField()
    
    # Estagiários
    estagiarios = serializers.SerializerMethodField()
    
    # Estatísticas
    estatisticas = serializers.SerializerMethodField()

    def get_cnpj_formatado(self, obj):
        """Retorna o CNPJ formatado."""
        cnpj = obj.cnpj
        if len(cnpj) == 14:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        return cnpj

    def get_terceirizados(self, obj):
        """Retorna os terceirizados da empresa."""
        from django.utils import timezone
        from django.db.models import Q
        
        hoje = timezone.now().date()
        terceirizados = obj.terceirizados.select_related('usuario').all()
        
        return [
            {
                'usuario_id': t.usuario.id,
                'nome': t.usuario.nome,
                'cpf': t.usuario.cpf,
                'data_inicio_contrato': t.data_inicio_contrato,
                'data_fim_contrato': t.data_fim_contrato,
                'contrato_ativo': t.data_fim_contrato is None or t.data_fim_contrato >= hoje,
            }
            for t in terceirizados
        ]

    def get_estagiarios(self, obj):
        """Retorna os estagiários da empresa."""
        from django.utils import timezone
        
        hoje = timezone.now().date()
        estagiarios = obj.estagiarios.select_related('usuario', 'curso').all()
        
        return [
            {
                'usuario_id': e.usuario.id,
                'nome': e.usuario.nome,
                'cpf': e.usuario.cpf,
                'curso': e.curso.nome,
                'carga_horaria': e.carga_horaria,
                'data_inicio_estagio': e.data_inicio_estagio,
                'data_fim_estagio': e.data_fim_estagio,
                'estagio_ativo': e.data_fim_estagio is None or e.data_fim_estagio >= hoje,
            }
            for e in estagiarios
        ]

    def get_estatisticas(self, obj):
        """Retorna estatísticas da empresa."""
        from django.utils import timezone
        from django.db.models import Q
        
        hoje = timezone.now().date()
        
        terceirizados_ativos = obj.terceirizados.filter(
            Q(data_fim_contrato__isnull=True) | Q(data_fim_contrato__gte=hoje)
        ).count()
        
        estagiarios_ativos = obj.estagiarios.filter(
            Q(data_fim_estagio__isnull=True) | Q(data_fim_estagio__gte=hoje)
        ).count()
        
        return {
            'total_terceirizados': obj.terceirizados.count(),
            'terceirizados_ativos': terceirizados_ativos,
            'total_estagiarios': obj.estagiarios.count(),
            'estagiarios_ativos': estagiarios_ativos,
            'total_vinculos': obj.terceirizados.count() + obj.estagiarios.count(),
            'vinculos_ativos': terceirizados_ativos + estagiarios_ativos,
        }


# ============================================================================
# SERIALIZERS PARA ESTATÍSTICAS
# ============================================================================

class EstatisticasEmpresasSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de empresas.
    """
    total_empresas = serializers.IntegerField(read_only=True)
    total_ativas = serializers.IntegerField(read_only=True)
    total_inativas = serializers.IntegerField(read_only=True)
    total_terceirizados = serializers.IntegerField(read_only=True)
    total_estagiarios = serializers.IntegerField(read_only=True)
    empresas_por_quantidade_vinculos = serializers.ListField(read_only=True)


# ============================================================================
# SERIALIZERS DE INPUT (Criação/Edição)
# ============================================================================

class EmpresaCriarSerializer(serializers.Serializer):
    """
    Serializer para criação de uma nova empresa.
    
    **Campos obrigatórios:**
    - nome: Nome da empresa
    - cnpj: CNPJ da empresa (14 dígitos, apenas números)
    
    **Campos opcionais:**
    - is_active: Se a empresa está ativa (padrão: True)
    """
    nome = serializers.CharField(
        max_length=255,
        help_text='Nome da empresa'
    )
    cnpj = serializers.CharField(
        max_length=14,
        min_length=14,
        help_text='CNPJ da empresa (14 dígitos, apenas números)'
    )
    is_active = serializers.BooleanField(
        default=True,
        required=False,
        help_text='Se a empresa está ativa'
    )

    def validate_cnpj(self, value):
        """Valida se o CNPJ contém apenas números e tem 14 dígitos."""
        if not value.isdigit():
            raise serializers.ValidationError('O CNPJ deve conter apenas números.')
        if len(value) != 14:
            raise serializers.ValidationError('O CNPJ deve ter exatamente 14 dígitos.')
        
        from EstruturaOrganizacional.empresa.models import Empresa
        if Empresa.objects.filter(cnpj=value).exists():
            raise serializers.ValidationError('Já existe uma empresa com este CNPJ.')
        
        return value


class EmpresaEditarSerializer(serializers.Serializer):
    """
    Serializer para edição de uma empresa existente.
    
    **Campos opcionais:**
    - nome: Nome da empresa
    - cnpj: CNPJ da empresa (14 dígitos, apenas números)
    - is_active: Se a empresa está ativa
    """
    nome = serializers.CharField(
        max_length=255,
        required=False,
        help_text='Nome da empresa'
    )
    cnpj = serializers.CharField(
        max_length=14,
        min_length=14,
        required=False,
        help_text='CNPJ da empresa (14 dígitos, apenas números)'
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text='Se a empresa está ativa'
    )

    def validate_cnpj(self, value):
        """Valida se o CNPJ contém apenas números e tem 14 dígitos."""
        if not value.isdigit():
            raise serializers.ValidationError('O CNPJ deve conter apenas números.')
        if len(value) != 14:
            raise serializers.ValidationError('O CNPJ deve ter exatamente 14 dígitos.')
        return value

    def validate(self, attrs):
        """Valida se o CNPJ já existe (exceto para a própria empresa)."""
        cnpj = attrs.get('cnpj')
        if cnpj:
            from EstruturaOrganizacional.empresa.models import Empresa
            instance = self.context.get('instance')
            queryset = Empresa.objects.filter(cnpj=cnpj)
            if instance:
                queryset = queryset.exclude(pk=instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({'cnpj': 'Já existe uma empresa com este CNPJ.'})
        return attrs
