from rest_framework import serializers

from Usuarios.usuario.serializers import (
    CampusResumoSerializer,
    ContatoListaSerializer,
    EnderecoListaSerializer,
    EmpresaResumoSerializer,
    UsuarioSetorResumoSerializer,
)


# ============================================================================
# SERIALIZERS DE USUÁRIO BASE PARA TERCEIRIZADO
# ============================================================================

class UsuarioBaseTerceirizadoSerializer(serializers.Serializer):
    """
    Serializer do usuário base para uso nos serializers de Terceirizado.
    
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


class UsuarioCompletoTerceirizadoSerializer(UsuarioBaseTerceirizadoSerializer):
    """
    Serializer completo do usuário base para Terceirizado.
    
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
# SERIALIZERS DE TERCEIRIZADO
# ============================================================================

class TerceirizadoListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de terceirizados (versão resumida).
    
    Ideal para endpoints de listagem onde não é necessário
    carregar todos os dados relacionados.
    """
    # Identificação (usa o pk do usuário)
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    cpf = serializers.CharField(source='usuario.cpf', read_only=True)
    
    # Dados do terceirizado
    empresa = EmpresaResumoSerializer(read_only=True)
    data_inicio_contrato = serializers.DateField(read_only=True)
    data_fim_contrato = serializers.DateField(read_only=True, allow_null=True)
    
    # Campus do usuário
    campus = CampusResumoSerializer(source='usuario.campus', read_only=True)
    
    # Status
    ativo = serializers.BooleanField(source='usuario.ativo', read_only=True)
    contrato_ativo = serializers.SerializerMethodField()

    def get_contrato_ativo(self, obj):
        """Verifica se o contrato está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_contrato is None:
            return True
        return obj.data_fim_contrato >= timezone.now().date()


class TerceirizadoDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um terceirizado.
    
    Inclui:
    - Dados específicos do terceirizado
    - Informações da empresa
    - Informações completas do usuário base
    - Contatos e endereços
    - Setores vinculados
    - Métricas de contrato
    """
    # Identificação
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    
    # Dados do contrato
    empresa = EmpresaResumoSerializer(read_only=True)
    data_inicio_contrato = serializers.DateField(read_only=True)
    data_fim_contrato = serializers.DateField(read_only=True, allow_null=True)
    
    # Status do contrato
    contrato_ativo = serializers.SerializerMethodField()
    tempo_contrato_dias = serializers.SerializerMethodField()
    tempo_contrato_meses = serializers.SerializerMethodField()
    dias_restantes_contrato = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Dados do usuário base
    usuario = UsuarioCompletoTerceirizadoSerializer(read_only=True)

    def get_contrato_ativo(self, obj):
        """Verifica se o contrato está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_contrato is None:
            return True
        return obj.data_fim_contrato >= timezone.now().date()

    def get_tempo_contrato_dias(self, obj):
        """Calcula o tempo de contrato em dias."""
        from django.utils import timezone
        
        data_fim = obj.data_fim_contrato if obj.data_fim_contrato else timezone.now().date()
        delta = data_fim - obj.data_inicio_contrato
        return delta.days

    def get_tempo_contrato_meses(self, obj):
        """Calcula o tempo de contrato em meses."""
        from django.utils import timezone
        
        data_fim = obj.data_fim_contrato if obj.data_fim_contrato else timezone.now().date()
        delta = data_fim - obj.data_inicio_contrato
        return delta.days // 30

    def get_dias_restantes_contrato(self, obj):
        """Calcula os dias restantes do contrato."""
        from django.utils import timezone
        
        if obj.data_fim_contrato is None:
            return None
        
        hoje = timezone.now().date()
        if obj.data_fim_contrato < hoje:
            return 0
        
        delta = obj.data_fim_contrato - hoje
        return delta.days


class TerceirizadoResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de terceirizado para uso em nested serializers.
    
    Contém informações essenciais para identificação.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    contrato_ativo = serializers.SerializerMethodField()

    def get_contrato_ativo(self, obj):
        """Verifica se o contrato está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_contrato is None:
            return True
        return obj.data_fim_contrato >= timezone.now().date()


# ============================================================================
# SERIALIZERS PARA CONSULTAS ESPECÍFICAS
# ============================================================================

class TerceirizadoPorEmpresaSerializer(serializers.Serializer):
    """
    Serializer para listagem de terceirizados de uma empresa.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    cpf = serializers.CharField(source='usuario.cpf', read_only=True)
    data_inicio_contrato = serializers.DateField(read_only=True)
    data_fim_contrato = serializers.DateField(read_only=True, allow_null=True)
    contrato_ativo = serializers.SerializerMethodField()

    def get_contrato_ativo(self, obj):
        """Verifica se o contrato está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_contrato is None:
            return True
        return obj.data_fim_contrato >= timezone.now().date()


class EmpresaComTerceirizadosSerializer(serializers.Serializer):
    """
    Serializer para visualizar empresa com seus terceirizados.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    cnpj_formatado = serializers.SerializerMethodField()
    ativo = serializers.BooleanField(read_only=True)
    
    # Terceirizados
    terceirizados = TerceirizadoPorEmpresaSerializer(many=True, read_only=True)
    total_terceirizados = serializers.SerializerMethodField()
    total_contratos_ativos = serializers.SerializerMethodField()

    def get_cnpj_formatado(self, obj):
        """Retorna o CNPJ formatado (XX.XXX.XXX/XXXX-XX)."""
        cnpj = obj.cnpj
        if len(cnpj) == 14:
            return f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'
        return cnpj

    def get_total_terceirizados(self, obj):
        """Retorna o total de terceirizados da empresa."""
        return obj.terceirizados.count()

    def get_total_contratos_ativos(self, obj):
        """Retorna o total de contratos ativos."""
        from django.utils import timezone
        from django.db.models import Q
        
        hoje = timezone.now().date()
        return obj.terceirizados.filter(
            Q(data_fim_contrato__isnull=True) | Q(data_fim_contrato__gte=hoje)
        ).count()


class ContratosVencendoSerializer(serializers.Serializer):
    """
    Serializer para terceirizados com contratos próximos do vencimento.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    empresa = EmpresaResumoSerializer(read_only=True)
    data_fim_contrato = serializers.DateField(read_only=True)
    dias_restantes = serializers.SerializerMethodField()

    def get_dias_restantes(self, obj):
        """Calcula os dias restantes do contrato."""
        from django.utils import timezone
        
        if obj.data_fim_contrato is None:
            return None
        
        delta = obj.data_fim_contrato - timezone.now().date()
        return delta.days
