from rest_framework import serializers

from Usuarios.usuario.serializers import (
    CampusResumoSerializer,
    ContatoListaSerializer,
    EnderecoListaSerializer,
    UsuarioSetorResumoSerializer,
)


# ============================================================================
# SERIALIZERS DE USUÁRIO BASE PARA SERVIDOR
# ============================================================================

class UsuarioBaseServidorSerializer(serializers.Serializer):
    """
    Serializer do usuário base para uso nos serializers de Servidor.
    
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
    is_admin = serializers.BooleanField(read_only=True)
    last_login = serializers.DateField(read_only=True, allow_null=True)
    campus = CampusResumoSerializer(read_only=True)

    def get_cpf_formatado(self, obj):
        """Retorna o CPF formatado (XXX.XXX.XXX-XX)."""
        cpf = obj.cpf
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf


class UsuarioCompletoServidorSerializer(UsuarioBaseServidorSerializer):
    """
    Serializer completo do usuário base para Servidor.
    
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
# SERIALIZERS DE SERVIDOR
# ============================================================================

class ServidorListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de servidores (versão resumida).
    
    Ideal para endpoints de listagem onde não é necessário
    carregar todos os dados relacionados.
    """
    # Identificação (usa o pk do usuário)
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    cpf = serializers.CharField(source='usuario.cpf', read_only=True)
    
    # Dados do servidor
    tipo_servidor = serializers.CharField(read_only=True)
    jornada_trabalho = serializers.IntegerField(read_only=True)
    jornada_trabalho_display = serializers.SerializerMethodField()
    classe = serializers.CharField(read_only=True)
    
    # Campus do usuário
    campus = CampusResumoSerializer(source='usuario.campus', read_only=True)
    
    # Status
    ativo = serializers.BooleanField(source='usuario.ativo', read_only=True)

    def get_jornada_trabalho_display(self, obj):
        """Retorna a descrição legível da jornada de trabalho."""
        return obj.get_jornada_trabalho_display()


class ServidorDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um servidor.
    
    Inclui:
    - Dados específicos do servidor
    - Informações completas do usuário base
    - Contatos e endereços
    - Setores vinculados
    - Métricas calculadas
    """
    # Identificação
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    
    # Dados do servidor
    data_posse = serializers.DateField(read_only=True)
    jornada_trabalho = serializers.IntegerField(read_only=True)
    jornada_trabalho_display = serializers.SerializerMethodField()
    padrao = serializers.CharField(read_only=True)
    classe = serializers.CharField(read_only=True)
    tipo_servidor = serializers.CharField(read_only=True)
    
    # Métricas calculadas
    tempo_servico_anos = serializers.SerializerMethodField()
    tempo_servico_dias = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Dados do usuário base
    usuario = UsuarioCompletoServidorSerializer(read_only=True)

    def get_jornada_trabalho_display(self, obj):
        """Retorna a descrição legível da jornada de trabalho."""
        return obj.get_jornada_trabalho_display()

    def get_tempo_servico_anos(self, obj):
        """Calcula o tempo de serviço em anos."""
        from django.utils import timezone
        
        hoje = timezone.now().date()
        delta = hoje - obj.data_posse
        return delta.days // 365

    def get_tempo_servico_dias(self, obj):
        """Calcula o tempo de serviço em dias."""
        from django.utils import timezone
        
        hoje = timezone.now().date()
        delta = hoje - obj.data_posse
        return delta.days


class ServidorResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de servidor para uso em nested serializers.
    
    Contém informações essenciais para identificação.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    tipo_servidor = serializers.CharField(read_only=True)
    classe = serializers.CharField(read_only=True)
    jornada_trabalho_display = serializers.SerializerMethodField()

    def get_jornada_trabalho_display(self, obj):
        """Retorna a descrição legível da jornada de trabalho."""
        return obj.get_jornada_trabalho_display()


# ============================================================================
# SERIALIZERS PARA CONSULTAS ESPECÍFICAS
# ============================================================================

class ServidorPorTipoSerializer(serializers.Serializer):
    """
    Serializer para listagem de servidores agrupados por tipo.
    
    Ideal para endpoints que retornam estatísticas por tipo de servidor.
    """
    tipo_servidor = serializers.CharField(read_only=True)
    quantidade = serializers.IntegerField(read_only=True)
    servidores = ServidorResumoSerializer(many=True, read_only=True)


class ServidorPorJornadaSerializer(serializers.Serializer):
    """
    Serializer para listagem de servidores agrupados por jornada.
    """
    jornada_trabalho = serializers.IntegerField(read_only=True)
    jornada_trabalho_display = serializers.CharField(read_only=True)
    quantidade = serializers.IntegerField(read_only=True)
