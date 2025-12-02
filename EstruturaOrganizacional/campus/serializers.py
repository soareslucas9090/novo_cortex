from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers


# ============================================================================
# SERIALIZERS DE CAMPUS
# ============================================================================

class CampusListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de campi (versão resumida).
    
    Ideal para endpoints de listagem e seletores.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    cnpj_formatado = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)

    @extend_schema_field(serializers.CharField())
    def get_cnpj_formatado(self, obj) -> str:
        """Retorna o CNPJ formatado (XX.XXX.XXX/XXXX-XX)."""
        cnpj = obj.cnpj
        if len(cnpj) == 14:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        return cnpj


class CampusDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um campus.
    
    Inclui:
    - Dados do campus
    - Estatísticas de usuários
    - Timestamps
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    cnpj_formatado = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    
    # Estatísticas
    total_usuarios = serializers.SerializerMethodField()
    total_usuarios_ativos = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_cnpj_formatado(self, obj):
        """Retorna o CNPJ formatado (XX.XXX.XXX/XXXX-XX)."""
        cnpj = obj.cnpj
        if len(cnpj) == 14:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        return cnpj

    def get_total_usuarios(self, obj):
        """Retorna o total de usuários do campus."""
        return obj.usuarios.count()

    def get_total_usuarios_ativos(self, obj):
        """Retorna o total de usuários ativos do campus."""
        return obj.usuarios.filter(is_active=True).count()


class CampusResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de campus para uso em nested serializers.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class CampusComUsuariosSerializer(serializers.Serializer):
    """
    Serializer para visualizar campus com estatísticas de usuários por perfil.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    cnpj_formatado = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    
    # Estatísticas por perfil
    estatisticas = serializers.SerializerMethodField()

    def get_cnpj_formatado(self, obj):
        """Retorna o CNPJ formatado."""
        cnpj = obj.cnpj
        if len(cnpj) == 14:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        return cnpj

    def get_estatisticas(self, obj):
        """Retorna estatísticas de usuários por perfil."""
        usuarios = obj.usuarios.all()
        
        total = usuarios.count()
        ativos = usuarios.filter(is_active=True).count()
        
        # Contagem por perfil
        servidores = 0
        alunos = 0
        terceirizados = 0
        estagiarios = 0
        
        for usuario in usuarios:
            try:
                if hasattr(usuario, 'servidor') and usuario.servidor:
                    servidores += 1
            except:
                pass
            try:
                if hasattr(usuario, 'aluno') and usuario.aluno:
                    alunos += 1
            except:
                pass
            try:
                if hasattr(usuario, 'terceirizado') and usuario.terceirizado:
                    terceirizados += 1
            except:
                pass
            try:
                if hasattr(usuario, 'estagiario') and usuario.estagiario:
                    estagiarios += 1
            except:
                pass
        
        return {
            'total': total,
            'ativos': ativos,
            'inativos': total - ativos,
            'por_perfil': {
                'servidores': servidores,
                'alunos': alunos,
                'terceirizados': terceirizados,
                'estagiarios': estagiarios,
            }
        }


# ============================================================================
# SERIALIZERS PARA ESTATÍSTICAS
# ============================================================================

class EstatisticasCampusSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de campi.
    """
    total_campi = serializers.IntegerField(read_only=True)
    total_ativos = serializers.IntegerField(read_only=True)
    total_inativos = serializers.IntegerField(read_only=True)
    campi = CampusListaSerializer(many=True, read_only=True)


# ============================================================================
# SERIALIZERS DE INPUT (Criação/Edição)
# ============================================================================

class CampusCriarSerializer(serializers.Serializer):
    """
    Serializer para criação de um novo campus.
    
    **Campos obrigatórios:**
    - nome: Nome do campus
    - cnpj: CNPJ do campus (14 dígitos, apenas números)
    
    **Campos opcionais:**
    - is_active: Se o campus está ativo (padrão: True)
    """
    nome = serializers.CharField(
        max_length=255,
        help_text='Nome do campus'
    )
    cnpj = serializers.CharField(
        max_length=14,
        min_length=14,
        help_text='CNPJ do campus (14 dígitos, apenas números)'
    )
    is_active = serializers.BooleanField(
        default=True,
        required=False,
        help_text='Se o campus está ativo'
    )

    def validate_cnpj(self, value):
        """Valida se o CNPJ contém apenas números e tem 14 dígitos."""
        if not value.isdigit():
            raise serializers.ValidationError('O CNPJ deve conter apenas números.')
        if len(value) != 14:
            raise serializers.ValidationError('O CNPJ deve ter exatamente 14 dígitos.')
        
        from EstruturaOrganizacional.campus.models import Campus
        if Campus.objects.filter(cnpj=value).exists():
            raise serializers.ValidationError('Já existe um campus com este CNPJ.')
        
        return value


class CampusEditarSerializer(serializers.Serializer):
    """
    Serializer para edição de um campus existente.
    
    **Campos opcionais:**
    - nome: Nome do campus
    - cnpj: CNPJ do campus (14 dígitos, apenas números)
    - is_active: Se o campus está ativo
    """
    nome = serializers.CharField(
        max_length=255,
        required=False,
        help_text='Nome do campus'
    )
    cnpj = serializers.CharField(
        max_length=14,
        min_length=14,
        required=False,
        help_text='CNPJ do campus (14 dígitos, apenas números)'
    )
    is_active = serializers.BooleanField(
        required=False,
        help_text='Se o campus está ativo'
    )

    def validate_cnpj(self, value):
        """Valida se o CNPJ contém apenas números e tem 14 dígitos."""
        if not value.isdigit():
            raise serializers.ValidationError('O CNPJ deve conter apenas números.')
        if len(value) != 14:
            raise serializers.ValidationError('O CNPJ deve ter exatamente 14 dígitos.')
        return value

    def validate(self, attrs):
        """Valida se o CNPJ já existe (exceto para o próprio campus)."""
        cnpj = attrs.get('cnpj')
        if cnpj:
            from EstruturaOrganizacional.campus.models import Campus
            instance = self.context.get('instance')
            queryset = Campus.objects.filter(cnpj=cnpj)
            if instance:
                queryset = queryset.exclude(pk=instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({'cnpj': 'Já existe um campus com este CNPJ.'})
        return attrs
