from rest_framework import serializers


# ============================================================================
# SERIALIZERS DE ENTIDADES RELACIONADAS (Campus, Setor, Empresa, Curso)
# ============================================================================

class CampusResumoSerializer(serializers.Serializer):
    """Serializer resumido do Campus para uso em nested serializers."""
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class SetorResumoSerializer(serializers.Serializer):
    """Serializer resumido do Setor para uso em nested serializers."""
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class EmpresaResumoSerializer(serializers.Serializer):
    """Serializer resumido da Empresa para uso em nested serializers."""
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cnpj = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)


class CursoResumoSerializer(serializers.Serializer):
    """Serializer resumido do Curso para uso em nested serializers."""
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    descricao = serializers.CharField(read_only=True, allow_null=True)


# ============================================================================
# SERIALIZERS DE CONTATO E ENDEREÇO
# ============================================================================

class ContatoSerializer(serializers.Serializer):
    """
    Serializer para visualização de contatos do usuário.
    
    Retorna informações completas de contato (email e telefone).
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True, allow_null=True)
    telefone = serializers.CharField(read_only=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class ContatoListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de contatos (versão resumida).
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True, allow_null=True)
    telefone = serializers.CharField(read_only=True, allow_null=True)


class EnderecoSerializer(serializers.Serializer):
    """
    Serializer para visualização de endereços do usuário.
    
    Retorna informações completas do endereço.
    """
    id = serializers.IntegerField(read_only=True)
    logradouro = serializers.CharField(read_only=True)
    bairro = serializers.CharField(read_only=True)
    cep = serializers.CharField(read_only=True)
    num_casa = serializers.CharField(read_only=True)
    cidade = serializers.CharField(read_only=True)
    estado = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    endereco_completo = serializers.SerializerMethodField()

    def get_endereco_completo(self, obj):
        """Retorna o endereço formatado completo."""
        return f'{obj.logradouro}, {obj.num_casa} - {obj.bairro}, {obj.cidade}/{obj.estado} - CEP: {obj.cep}'


class EnderecoListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de endereços (versão resumida).
    """
    id = serializers.IntegerField(read_only=True)
    logradouro = serializers.CharField(read_only=True)
    num_casa = serializers.CharField(read_only=True)
    cidade = serializers.CharField(read_only=True)
    estado = serializers.CharField(read_only=True)


# ============================================================================
# SERIALIZERS DE PERFIS (Servidor, Aluno, Terceirizado, Estagiário)
# ============================================================================

class ServidorPerfilSerializer(serializers.Serializer):
    """
    Serializer para visualização do perfil de Servidor.
    
    Inclui todas as informações específicas do servidor.
    """
    data_posse = serializers.DateField(read_only=True)
    jornada_trabalho = serializers.IntegerField(read_only=True)
    jornada_trabalho_display = serializers.SerializerMethodField()
    padrao = serializers.CharField(read_only=True)
    classe = serializers.CharField(read_only=True)
    tipo_servidor = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_jornada_trabalho_display(self, obj):
        """Retorna a descrição legível da jornada de trabalho."""
        return obj.get_jornada_trabalho_display()


class AlunoPerfilSerializer(serializers.Serializer):
    """
    Serializer para visualização do perfil de Aluno.
    
    Inclui todas as informações específicas do aluno.
    """
    ira = serializers.DecimalField(max_digits=4, decimal_places=2, read_only=True)
    forma_ingresso = serializers.CharField(read_only=True)
    forma_ingresso_display = serializers.SerializerMethodField()
    previsao_conclusao = serializers.IntegerField(read_only=True)
    aluno_especial = serializers.BooleanField(read_only=True)
    turno = serializers.CharField(read_only=True)
    turno_display = serializers.SerializerMethodField()
    is_active = serializers.BooleanField(read_only=True)
    ano_conclusao = serializers.IntegerField(read_only=True, allow_null=True)
    data_colacao = serializers.DateField(read_only=True, allow_null=True)
    data_expedicao_diploma = serializers.DateField(read_only=True, allow_null=True)
    is_formado = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_forma_ingresso_display(self, obj):
        """Retorna a descrição legível da forma de ingresso."""
        return obj.get_forma_ingresso_display()

    def get_turno_display(self, obj):
        """Retorna a descrição legível do turno."""
        return obj.get_turno_display()


class TerceirizadoPerfilSerializer(serializers.Serializer):
    """
    Serializer para visualização do perfil de Terceirizado.
    
    Inclui informações específicas e a empresa associada.
    """
    empresa = EmpresaResumoSerializer(read_only=True)
    data_inicio_contrato = serializers.DateField(read_only=True)
    data_fim_contrato = serializers.DateField(read_only=True, allow_null=True)
    contrato_ativo = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_contrato_ativo(self, obj):
        """Verifica se o contrato está ativo (sem data de fim ou data futura)."""
        from django.utils import timezone
        if obj.data_fim_contrato is None:
            return True
        return obj.data_fim_contrato >= timezone.now().date()


class EstagiarioPerfilSerializer(serializers.Serializer):
    """
    Serializer para visualização do perfil de Estagiário.
    
    Inclui informações específicas, empresa e curso associados.
    """
    empresa = EmpresaResumoSerializer(read_only=True)
    curso = CursoResumoSerializer(read_only=True)
    carga_horaria = serializers.IntegerField(read_only=True)
    data_inicio_estagio = serializers.DateField(read_only=True)
    data_fim_estagio = serializers.DateField(read_only=True, allow_null=True)
    estagio_ativo = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_estagio_ativo(self, obj):
        """Verifica se o estágio está ativo (sem data de fim ou data futura)."""
        from django.utils import timezone
        if obj.data_fim_estagio is None:
            return True
        return obj.data_fim_estagio >= timezone.now().date()


# ============================================================================
# SERIALIZERS DE USUÁRIO
# ============================================================================

class UsuarioSetorResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de UsuarioSetor para uso em nested serializers.
    
    Inclui informações do setor e do vínculo.
    """
    id = serializers.IntegerField(read_only=True)
    setor = SetorResumoSerializer(read_only=True)
    campus = CampusResumoSerializer(read_only=True)
    e_responsavel = serializers.BooleanField(read_only=True)
    monitor = serializers.BooleanField(read_only=True)
    data_entrada = serializers.DateField(read_only=True)
    data_saida = serializers.DateField(read_only=True, allow_null=True)
    vinculo_ativo = serializers.SerializerMethodField()

    def get_vinculo_ativo(self, obj):
        """Verifica se o vínculo com o setor está ativo."""
        return obj.data_saida is None


class UsuarioListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de usuários (versão resumida).
    
    Ideal para endpoints de listagem onde não é necessário
    carregar todos os dados relacionados.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cpf = serializers.CharField(read_only=True)
    campus = CampusResumoSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    tipo_perfil = serializers.SerializerMethodField()

    def get_tipo_perfil(self, obj):
        """Retorna o tipo de perfil do usuário."""
        tipos = []
        if hasattr(obj, 'servidor') and obj.servidor:
            tipos.append('Servidor')
        if hasattr(obj, 'aluno') and obj.aluno:
            tipos.append('Aluno')
        if hasattr(obj, 'terceirizado') and obj.terceirizado:
            tipos.append('Terceirizado')
        if hasattr(obj, 'estagiario') and obj.estagiario:
            tipos.append('Estagiário')
        return tipos if tipos else ['Sem perfil']


class SetorComAtividadesFuncoesSerializer(serializers.Serializer):
    """
    Serializer de setor que inclui atividades e funções.
    
    Usado em nested serializers para mostrar a hierarquia completa.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    atividades = serializers.SerializerMethodField()

    def get_atividades(self, obj):
        """Retorna as atividades do setor com suas funções."""
        atividades_data = []
        for atividade in obj.atividades.prefetch_related('funcoes').all():
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
            }
            atividades_data.append(atividade_item)
        return atividades_data


class UsuarioSetorComAtividadesSerializer(serializers.Serializer):
    """
    Serializer de UsuarioSetor que inclui o setor com atividades e funções.
    
    Usado para mostrar vínculos completos do usuário.
    """
    id = serializers.IntegerField(read_only=True)
    setor = SetorComAtividadesFuncoesSerializer(read_only=True)
    campus = CampusResumoSerializer(read_only=True)
    e_responsavel = serializers.BooleanField(read_only=True)
    monitor = serializers.BooleanField(read_only=True)
    data_entrada = serializers.DateField(read_only=True)
    data_saida = serializers.DateField(read_only=True, allow_null=True)
    vinculo_ativo = serializers.SerializerMethodField()

    def get_vinculo_ativo(self, obj):
        """Verifica se o vínculo com o setor está ativo."""
        return obj.data_saida is None


class UsuarioListaDetalhadaSerializer(serializers.Serializer):
    """
    Serializer para listagem de usuários com detalhes de setores e atividades.
    
    Inclui:
    - Dados básicos do usuário
    - Campus
    - Tipo de perfil
    - Setores vinculados com suas atividades e funções
    - Contatos
    
    Ideal para listagens onde é necessário visualizar a estrutura
    organizacional completa de cada usuário.
    """
    # Identificação
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cpf = serializers.CharField(read_only=True)
    cpf_formatado = serializers.SerializerMethodField()
    
    # Dados pessoais
    data_nascimento = serializers.DateField(read_only=True)
    data_ingresso = serializers.DateField(read_only=True, allow_null=True)
    
    # Status
    is_active = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    
    # Relacionamentos
    campus = CampusResumoSerializer(read_only=True)
    tipo_perfil = serializers.SerializerMethodField()
    
    # Contatos
    contatos = serializers.SerializerMethodField()
    
    # Setores com atividades e funções
    setores = serializers.SerializerMethodField()
    total_setores_ativos = serializers.SerializerMethodField()

    def get_contatos(self, obj):
        """Retorna os contatos do usuário."""
        return ContatoListaSerializer(obj.contatos.all(), many=True).data

    def get_cpf_formatado(self, obj):
        """Retorna o CPF formatado (XXX.XXX.XXX-XX)."""
        cpf = obj.cpf
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf

    def get_tipo_perfil(self, obj):
        """Retorna o(s) tipo(s) de perfil do usuário."""
        tipos = []
        try:
            if hasattr(obj, 'servidor') and obj.servidor:
                tipos.append('Servidor')
        except:
            pass
        try:
            if hasattr(obj, 'aluno') and obj.aluno:
                tipos.append('Aluno')
        except:
            pass
        try:
            if hasattr(obj, 'terceirizado') and obj.terceirizado:
                tipos.append('Terceirizado')
        except:
            pass
        try:
            if hasattr(obj, 'estagiario') and obj.estagiario:
                tipos.append('Estagiário')
        except:
            pass
        return tipos if tipos else ['Sem perfil']

    def get_setores(self, obj):
        """Retorna os setores vinculados ao usuário com atividades e funções."""
        usuario_setores = obj.usuario_setores.select_related(
            'setor', 'campus'
        ).prefetch_related(
            'setor__atividades',
            'setor__atividades__funcoes'
        ).all()
        return UsuarioSetorComAtividadesSerializer(usuario_setores, many=True).data

    def get_total_setores_ativos(self, obj):
        """Retorna o total de setores com vínculo ativo."""
        return obj.usuario_setores.filter(data_saida__isnull=True).count()


class UsuarioDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um usuário.
    
    Inclui:
    - Dados básicos do usuário
    - Informações do campus
    - Contatos
    - Endereços
    - Perfis (Servidor, Aluno, Terceirizado, Estagiário)
    - Setores vinculados
    
    Este serializer é ideal para endpoints de detalhe onde o frontend
    precisa de todas as informações do usuário em uma única requisição.
    """
    # Identificação
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cpf = serializers.CharField(read_only=True)
    cpf_formatado = serializers.SerializerMethodField()
    
    # Dados pessoais
    data_nascimento = serializers.DateField(read_only=True)
    data_ingresso = serializers.DateField(read_only=True, allow_null=True)
    
    # Status e permissões
    is_active = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_superuser = serializers.BooleanField(read_only=True)
    last_login = serializers.DateField(read_only=True, allow_null=True)
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    
    # Relacionamentos
    campus = CampusResumoSerializer(read_only=True)
    contatos = ContatoListaSerializer(many=True, read_only=True)
    enderecos = EnderecoListaSerializer(many=True, read_only=True)
    
    # Setores vinculados
    setores = serializers.SerializerMethodField()
    
    # Perfis
    tipo_perfil = serializers.SerializerMethodField()
    perfil_servidor = serializers.SerializerMethodField()
    perfil_aluno = serializers.SerializerMethodField()
    perfil_terceirizado = serializers.SerializerMethodField()
    perfil_estagiario = serializers.SerializerMethodField()

    def get_cpf_formatado(self, obj):
        """Retorna o CPF formatado (XXX.XXX.XXX-XX)."""
        cpf = obj.cpf
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf

    def get_setores(self, obj):
        """Retorna os setores vinculados ao usuário."""
        usuario_setores = obj.usuario_setores.select_related('setor', 'campus').all()
        return UsuarioSetorResumoSerializer(usuario_setores, many=True).data

    def get_tipo_perfil(self, obj):
        """Retorna o(s) tipo(s) de perfil do usuário."""
        tipos = []
        if hasattr(obj, 'servidor'):
            try:
                if obj.servidor:
                    tipos.append('Servidor')
            except:
                pass
        if hasattr(obj, 'aluno'):
            try:
                if obj.aluno:
                    tipos.append('Aluno')
            except:
                pass
        if hasattr(obj, 'terceirizado'):
            try:
                if obj.terceirizado:
                    tipos.append('Terceirizado')
            except:
                pass
        if hasattr(obj, 'estagiario'):
            try:
                if obj.estagiario:
                    tipos.append('Estagiário')
            except:
                pass
        return tipos if tipos else ['Sem perfil']

    def get_perfil_servidor(self, obj):
        """Retorna os dados do perfil de servidor, se existir."""
        try:
            if hasattr(obj, 'servidor') and obj.servidor:
                return ServidorPerfilSerializer(obj.servidor).data
        except:
            pass
        return None

    def get_perfil_aluno(self, obj):
        """Retorna os dados do perfil de aluno, se existir."""
        try:
            if hasattr(obj, 'aluno') and obj.aluno:
                return AlunoPerfilSerializer(obj.aluno).data
        except:
            pass
        return None

    def get_perfil_terceirizado(self, obj):
        """Retorna os dados do perfil de terceirizado, se existir."""
        try:
            if hasattr(obj, 'terceirizado') and obj.terceirizado:
                return TerceirizadoPerfilSerializer(obj.terceirizado).data
        except:
            pass
        return None

    def get_perfil_estagiario(self, obj):
        """Retorna os dados do perfil de estagiário, se existir."""
        try:
            if hasattr(obj, 'estagiario') and obj.estagiario:
                return EstagiarioPerfilSerializer(obj.estagiario).data
        except:
            pass
        return None


class UsuarioCompletoSerializer(UsuarioDetalheSerializer):
    """
    Serializer ultra-completo para visualização de usuário.
    
    Estende UsuarioDetalheSerializer adicionando contatos e endereços
    com informações completas (não resumidas).
    
    Ideal para páginas de perfil do próprio usuário ou admin.
    """
    contatos = ContatoSerializer(many=True, read_only=True)
    enderecos = EnderecoSerializer(many=True, read_only=True)


# ============================================================================
# SERIALIZERS DE REFERÊNCIA (para uso em outros apps)
# ============================================================================

class UsuarioReferenciaSerializer(serializers.Serializer):
    """
    Serializer mínimo para referência de usuário em outros serializers.
    
    Contém apenas id e nome para identificação.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cpf = serializers.CharField(read_only=True)


class UsuarioResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de usuário para uso em nested serializers.
    
    Inclui informações básicas e o tipo de perfil.
    """
    id = serializers.IntegerField(read_only=True)
    nome = serializers.CharField(read_only=True)
    cpf = serializers.CharField(read_only=True)
    cpf_formatado = serializers.SerializerMethodField()
    campus = CampusResumoSerializer(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    tipo_perfil = serializers.SerializerMethodField()

    def get_cpf_formatado(self, obj):
        """Retorna o CPF formatado (XXX.XXX.XXX-XX)."""
        cpf = obj.cpf
        if len(cpf) == 11:
            return f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
        return cpf

    def get_tipo_perfil(self, obj):
        """Retorna o(s) tipo(s) de perfil do usuário."""
        tipos = []
        try:
            if hasattr(obj, 'servidor') and obj.servidor:
                tipos.append('Servidor')
        except:
            pass
        try:
            if hasattr(obj, 'aluno') and obj.aluno:
                tipos.append('Aluno')
        except:
            pass
        try:
            if hasattr(obj, 'terceirizado') and obj.terceirizado:
                tipos.append('Terceirizado')
        except:
            pass
        try:
            if hasattr(obj, 'estagiario') and obj.estagiario:
                tipos.append('Estagiário')
        except:
            pass
        return tipos if tipos else ['Sem perfil']
