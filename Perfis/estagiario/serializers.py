from rest_framework import serializers

from Usuarios.usuario.serializers import (
    CampusResumoSerializer,
    ContatoListaSerializer,
    CursoResumoSerializer,
    EnderecoListaSerializer,
    EmpresaResumoSerializer,
    UsuarioSetorResumoSerializer,
)


# ============================================================================
# SERIALIZERS DE USUÁRIO BASE PARA ESTAGIÁRIO
# ============================================================================

class UsuarioBaseEstagiarioSerializer(serializers.Serializer):
    """
    Serializer do usuário base para uso nos serializers de Estagiário.
    
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


class UsuarioCompletoEstagiarioSerializer(UsuarioBaseEstagiarioSerializer):
    """
    Serializer completo do usuário base para Estagiário.
    
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
# SERIALIZERS DE ESTAGIÁRIO
# ============================================================================

class EstagiarioListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de estagiários (versão resumida).
    
    Ideal para endpoints de listagem onde não é necessário
    carregar todos os dados relacionados.
    """
    # Identificação (usa o pk do usuário)
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    cpf = serializers.CharField(source='usuario.cpf', read_only=True)
    
    # Dados do estagiário
    empresa = EmpresaResumoSerializer(read_only=True)
    curso = CursoResumoSerializer(read_only=True)
    carga_horaria = serializers.IntegerField(read_only=True)
    data_inicio_estagio = serializers.DateField(read_only=True)
    data_fim_estagio = serializers.DateField(read_only=True, allow_null=True)
    
    # Campus do usuário
    campus = CampusResumoSerializer(source='usuario.campus', read_only=True)
    
    # Status
    ativo = serializers.BooleanField(source='usuario.ativo', read_only=True)
    estagio_ativo = serializers.SerializerMethodField()

    def get_estagio_ativo(self, obj):
        """Verifica se o estágio está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_estagio is None:
            return True
        return obj.data_fim_estagio >= timezone.now().date()


class EstagiarioDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um estagiário.
    
    Inclui:
    - Dados específicos do estagiário
    - Informações da empresa e curso
    - Informações completas do usuário base
    - Contatos e endereços
    - Setores vinculados
    - Métricas do estágio
    """
    # Identificação
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    
    # Dados do estágio
    empresa = EmpresaResumoSerializer(read_only=True)
    curso = CursoResumoSerializer(read_only=True)
    carga_horaria = serializers.IntegerField(read_only=True)
    carga_horaria_mensal = serializers.SerializerMethodField()
    data_inicio_estagio = serializers.DateField(read_only=True)
    data_fim_estagio = serializers.DateField(read_only=True, allow_null=True)
    
    # Status do estágio
    estagio_ativo = serializers.SerializerMethodField()
    tempo_estagio_dias = serializers.SerializerMethodField()
    tempo_estagio_meses = serializers.SerializerMethodField()
    dias_restantes_estagio = serializers.SerializerMethodField()
    horas_totais_estimadas = serializers.SerializerMethodField()
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Dados do usuário base
    usuario = UsuarioCompletoEstagiarioSerializer(read_only=True)

    def get_carga_horaria_mensal(self, obj):
        """Calcula a carga horária mensal estimada (semanas * carga semanal)."""
        return obj.carga_horaria * 4

    def get_estagio_ativo(self, obj):
        """Verifica se o estágio está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_estagio is None:
            return True
        return obj.data_fim_estagio >= timezone.now().date()

    def get_tempo_estagio_dias(self, obj):
        """Calcula o tempo de estágio em dias."""
        from django.utils import timezone
        
        data_fim = obj.data_fim_estagio if obj.data_fim_estagio else timezone.now().date()
        delta = data_fim - obj.data_inicio_estagio
        return delta.days

    def get_tempo_estagio_meses(self, obj):
        """Calcula o tempo de estágio em meses."""
        from django.utils import timezone
        
        data_fim = obj.data_fim_estagio if obj.data_fim_estagio else timezone.now().date()
        delta = data_fim - obj.data_inicio_estagio
        return delta.days // 30

    def get_dias_restantes_estagio(self, obj):
        """Calcula os dias restantes do estágio."""
        from django.utils import timezone
        
        if obj.data_fim_estagio is None:
            return None
        
        hoje = timezone.now().date()
        if obj.data_fim_estagio < hoje:
            return 0
        
        delta = obj.data_fim_estagio - hoje
        return delta.days

    def get_horas_totais_estimadas(self, obj):
        """Calcula as horas totais estimadas do estágio."""
        from django.utils import timezone
        
        data_fim = obj.data_fim_estagio if obj.data_fim_estagio else timezone.now().date()
        delta = data_fim - obj.data_inicio_estagio
        semanas = delta.days // 7
        return semanas * obj.carga_horaria


class EstagiarioResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de estagiário para uso em nested serializers.
    
    Contém informações essenciais para identificação.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    curso_nome = serializers.CharField(source='curso.nome', read_only=True)
    empresa_nome = serializers.CharField(source='empresa.nome', read_only=True)
    carga_horaria = serializers.IntegerField(read_only=True)
    estagio_ativo = serializers.SerializerMethodField()

    def get_estagio_ativo(self, obj):
        """Verifica se o estágio está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_estagio is None:
            return True
        return obj.data_fim_estagio >= timezone.now().date()


# ============================================================================
# SERIALIZERS PARA CONSULTAS ESPECÍFICAS
# ============================================================================

class EstagiarioPorCursoSerializer(serializers.Serializer):
    """
    Serializer para listagem de estagiários de um curso.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    cpf = serializers.CharField(source='usuario.cpf', read_only=True)
    empresa = EmpresaResumoSerializer(read_only=True)
    carga_horaria = serializers.IntegerField(read_only=True)
    data_inicio_estagio = serializers.DateField(read_only=True)
    data_fim_estagio = serializers.DateField(read_only=True, allow_null=True)
    estagio_ativo = serializers.SerializerMethodField()

    def get_estagio_ativo(self, obj):
        """Verifica se o estágio está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_estagio is None:
            return True
        return obj.data_fim_estagio >= timezone.now().date()


class EstagiarioPorEmpresaSerializer(serializers.Serializer):
    """
    Serializer para listagem de estagiários de uma empresa.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    cpf = serializers.CharField(source='usuario.cpf', read_only=True)
    curso = CursoResumoSerializer(read_only=True)
    carga_horaria = serializers.IntegerField(read_only=True)
    data_inicio_estagio = serializers.DateField(read_only=True)
    data_fim_estagio = serializers.DateField(read_only=True, allow_null=True)
    estagio_ativo = serializers.SerializerMethodField()

    def get_estagio_ativo(self, obj):
        """Verifica se o estágio está ativo."""
        from django.utils import timezone
        
        if obj.data_fim_estagio is None:
            return True
        return obj.data_fim_estagio >= timezone.now().date()


class CursoComEstagiariosSerializer(serializers.Serializer):
    """
    Serializer para visualizar curso com seus estagiários.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    descricao = serializers.CharField(read_only=True, allow_null=True)
    
    # Estagiários
    estagiarios = EstagiarioPorCursoSerializer(many=True, read_only=True)
    total_estagiarios = serializers.SerializerMethodField()
    total_estagios_ativos = serializers.SerializerMethodField()

    def get_total_estagiarios(self, obj):
        """Retorna o total de estagiários do curso."""
        return obj.estagiarios.count()

    def get_total_estagios_ativos(self, obj):
        """Retorna o total de estágios ativos."""
        from django.utils import timezone
        from django.db.models import Q
        
        hoje = timezone.now().date()
        return obj.estagiarios.filter(
            Q(data_fim_estagio__isnull=True) | Q(data_fim_estagio__gte=hoje)
        ).count()


class EstagiosVencendoSerializer(serializers.Serializer):
    """
    Serializer para estagiários com estágios próximos do vencimento.
    """
    usuario_id = serializers.IntegerField(source='usuario.id', read_only=True)
    nome = serializers.CharField(source='usuario.nome', read_only=True)
    empresa = EmpresaResumoSerializer(read_only=True)
    curso = CursoResumoSerializer(read_only=True)
    data_fim_estagio = serializers.DateField(read_only=True)
    dias_restantes = serializers.SerializerMethodField()

    def get_dias_restantes(self, obj):
        """Calcula os dias restantes do estágio."""
        from django.utils import timezone
        
        if obj.data_fim_estagio is None:
            return None
        
        delta = obj.data_fim_estagio - timezone.now().date()
        return delta.days


class EstatisticasEstagiariosSerializer(serializers.Serializer):
    """
    Serializer para estatísticas gerais de estagiários.
    """
    total_estagiarios = serializers.IntegerField(read_only=True)
    total_estagios_ativos = serializers.IntegerField(read_only=True)
    total_estagios_encerrados = serializers.IntegerField(read_only=True)
    media_carga_horaria = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    por_curso = serializers.ListField(read_only=True)
    por_empresa = serializers.ListField(read_only=True)


# ============================================================================
# SERIALIZERS DE INPUT (Criação/Edição)
# ============================================================================

class EstagiarioCriarSerializer(serializers.Serializer):
    """
    Serializer para criação de um novo estagiário.
    
    **Campos obrigatórios:**
    - usuario_id: ID do usuário base
    - empresa_id: ID da empresa do estágio
    - curso_id: ID do curso
    - carga_horaria: Carga horária semanal
    - data_inicio_estagio: Data de início do estágio
    
    **Campos opcionais:**
    - data_fim_estagio: Data de fim do estágio
    """
    usuario_id = serializers.IntegerField(
        help_text='ID do usuário base'
    )
    empresa_id = serializers.IntegerField(
        help_text='ID da empresa do estágio'
    )
    curso_id = serializers.IntegerField(
        help_text='ID do curso'
    )
    carga_horaria = serializers.IntegerField(
        help_text='Carga horária semanal do estágio'
    )
    data_inicio_estagio = serializers.DateField(
        help_text='Data de início do estágio'
    )
    data_fim_estagio = serializers.DateField(
        required=False,
        allow_null=True,
        help_text='Data de fim do estágio'
    )

    def validate_usuario_id(self, value):
        """Valida se o usuário existe e se não é já um estagiário."""
        from Usuarios.usuario.models import Usuario
        from Perfis.estagiario.models import Estagiario
        
        try:
            usuario = Usuario.objects.get(pk=value)
        except Usuario.DoesNotExist:
            raise serializers.ValidationError('Usuário não encontrado.')
        
        if Estagiario.objects.filter(usuario_id=value).exists():
            raise serializers.ValidationError('Este usuário já possui um perfil de estagiário.')
        
        return value

    def validate_empresa_id(self, value):
        """Valida se a empresa existe."""
        from EstruturaOrganizacional.empresa.models import Empresa
        
        try:
            Empresa.objects.get(pk=value)
        except Empresa.DoesNotExist:
            raise serializers.ValidationError('Empresa não encontrada.')
        
        return value

    def validate_curso_id(self, value):
        """Valida se o curso existe."""
        from EstruturaOrganizacional.curso.models import Curso
        
        try:
            Curso.objects.get(pk=value)
        except Curso.DoesNotExist:
            raise serializers.ValidationError('Curso não encontrado.')
        
        return value

    def validate_carga_horaria(self, value):
        """Valida se a carga horária é válida."""
        if value <= 0:
            raise serializers.ValidationError('A carga horária deve ser maior que zero.')
        if value > 40:
            raise serializers.ValidationError('A carga horária não pode exceder 40 horas semanais.')
        return value

    def validate(self, attrs):
        """Valida se a data de fim é posterior à data de início."""
        data_inicio = attrs.get('data_inicio_estagio')
        data_fim = attrs.get('data_fim_estagio')
        
        if data_fim and data_inicio and data_fim < data_inicio:
            raise serializers.ValidationError({
                'data_fim_estagio': 'A data de fim deve ser posterior à data de início.'
            })
        
        return attrs


class EstagiarioEditarSerializer(serializers.Serializer):
    """
    Serializer para edição de um estagiário existente.
    
    **Campos opcionais:**
    - empresa_id: ID da empresa do estágio
    - curso_id: ID do curso
    - carga_horaria: Carga horária semanal
    - data_inicio_estagio: Data de início do estágio
    - data_fim_estagio: Data de fim do estágio
    """
    empresa_id = serializers.IntegerField(
        required=False,
        help_text='ID da empresa do estágio'
    )
    curso_id = serializers.IntegerField(
        required=False,
        help_text='ID do curso'
    )
    carga_horaria = serializers.IntegerField(
        required=False,
        help_text='Carga horária semanal do estágio'
    )
    data_inicio_estagio = serializers.DateField(
        required=False,
        help_text='Data de início do estágio'
    )
    data_fim_estagio = serializers.DateField(
        required=False,
        allow_null=True,
        help_text='Data de fim do estágio'
    )

    def validate_empresa_id(self, value):
        """Valida se a empresa existe."""
        if value is not None:
            from EstruturaOrganizacional.empresa.models import Empresa
            
            try:
                Empresa.objects.get(pk=value)
            except Empresa.DoesNotExist:
                raise serializers.ValidationError('Empresa não encontrada.')
        
        return value

    def validate_curso_id(self, value):
        """Valida se o curso existe."""
        if value is not None:
            from EstruturaOrganizacional.curso.models import Curso
            
            try:
                Curso.objects.get(pk=value)
            except Curso.DoesNotExist:
                raise serializers.ValidationError('Curso não encontrado.')
        
        return value

    def validate_carga_horaria(self, value):
        """Valida se a carga horária é válida."""
        if value is not None:
            if value <= 0:
                raise serializers.ValidationError('A carga horária deve ser maior que zero.')
            if value > 40:
                raise serializers.ValidationError('A carga horária não pode exceder 40 horas semanais.')
        return value

    def validate(self, attrs):
        """Valida se a data de fim é posterior à data de início."""
        data_inicio = attrs.get('data_inicio_estagio')
        data_fim = attrs.get('data_fim_estagio')
        
        # Se ambas as datas estão sendo atualizadas
        if data_fim and data_inicio and data_fim < data_inicio:
            raise serializers.ValidationError({
                'data_fim_estagio': 'A data de fim deve ser posterior à data de início.'
            })
        
        return attrs
