from drf_spectacular.utils import extend_schema

from rest_framework import status

from AppCore.basics.mixins.mixins import IsAdminMixin, IsOwnerOrAdminMixin
from AppCore.basics.views.basic_views import (
    BasicGetAPIView,
    BasicPostAPIView,
    BasicPutAPIView,
    BasicDeleteAPIView,
    BasicRetrieveAPIView,
)

from Perfis.estagiario.models import Estagiario
from Perfis.estagiario.serializers import (
    EstagiarioListaSerializer,
    EstagiarioDetalheSerializer,
    EstagiarioCriarSerializer,
    EstagiarioEditarSerializer,
)

from Usuarios.usuario.models import Usuario
from EstruturaOrganizacional.empresa.models import Empresa
from EstruturaOrganizacional.curso.models import Curso


# ============================================================================
# VIEWS DE ESTAGIÁRIO
# ============================================================================

@extend_schema(
    tags=['Perfis.Estagiario'],
    summary='Listar todos os estagiários',
    description='''
    Retorna uma lista paginada de todos os estagiários cadastrados no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - usuario_id, nome, cpf, empresa, curso, carga_horaria
    - data_inicio_estagio, data_fim_estagio, campus, ativo, estagio_ativo
    ''',
    responses={
        status.HTTP_200_OK: EstagiarioListaSerializer(many=True),
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class EstagiarioListaView(IsAdminMixin, BasicGetAPIView):
    """
    View para listagem de todos os estagiários.
    
    Apenas administradores podem visualizar todos os estagiários.
    Retorna uma lista resumida de todos os estagiários cadastrados.
    """
    serializer_class = EstagiarioListaSerializer
    mensagem_sucesso = 'Estagiários listados com sucesso.'

    def get_queryset(self):
        return Estagiario.objects.select_related(
            'usuario',
            'usuario__campus',
            'empresa',
            'curso'
        ).all()


@extend_schema(
    tags=['Perfis.Estagiario'],
    summary='Visualizar detalhes de um estagiário',
    description='''
    Retorna os dados completos de um estagiário específico.
    
    **Permissões:** 
    - Administradores podem visualizar qualquer estagiário
    - Usuários comuns podem visualizar apenas seu próprio perfil de estagiário
    
    **Retorno:**
    - Dados completos do estagiário incluindo empresa e curso
    - Informações do usuário base (contatos, endereços, setores)
    - Métricas calculadas do estágio
    ''',
    responses={
        status.HTTP_200_OK: EstagiarioDetalheSerializer,
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão'},
        status.HTTP_404_NOT_FOUND: {'description': 'Estagiário não encontrado'},
    },
)
class EstagiarioDetalheView(IsOwnerOrAdminMixin, BasicRetrieveAPIView):
    """
    View para visualização detalhada de um estagiário.
    
    Administradores podem ver qualquer estagiário.
    Usuários comuns podem ver apenas seu próprio perfil de estagiário.
    """
    serializer_class = EstagiarioDetalheSerializer
    mensagem_sucesso = 'Estagiário recuperado com sucesso.'
    queryset = Estagiario.objects.select_related(
        'usuario',
        'usuario__campus',
        'empresa',
        'curso'
    ).prefetch_related(
        'usuario__contatos',
        'usuario__enderecos',
        'usuario__usuario_setores',
        'usuario__usuario_setores__setor',
        'usuario__usuario_setores__campus',
    )
    lookup_field = 'pk'

    def obter_usuario_dono(self, obj):
        """Retorna o usuário dono do registro (para verificação de permissão)."""
        return obj.usuario


@extend_schema(
    tags=['Perfis.Estagiario'],
    summary='Criar um novo estagiário',
    description='''
    Cria um novo perfil de estagiário para um usuário existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - usuario_id: ID do usuário base
    - empresa_id: ID da empresa do estágio
    - curso_id: ID do curso
    - carga_horaria: Carga horária semanal
    - data_inicio_estagio: Data de início do estágio
    
    **Campos opcionais:**
    - data_fim_estagio: Data de fim do estágio
    ''',
    request=EstagiarioCriarSerializer,
    responses={
        status.HTTP_201_CREATED: {'description': 'Estagiário criado com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class EstagiarioCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de um novo estagiário.
    
    Apenas administradores podem criar estagiários.
    """
    serializer_class = EstagiarioCriarSerializer
    mensagem_sucesso = 'Estagiário criado com sucesso.'

    def do_action_post(self, serializer_data, request):
        # Busca as entidades relacionadas
        usuario = Usuario.objects.get(pk=serializer_data.pop('usuario_id'))
        empresa = Empresa.objects.get(pk=serializer_data.pop('empresa_id'))
        curso = Curso.objects.get(pk=serializer_data.pop('curso_id'))
        
        # Cria o estagiário
        Estagiario.objects.create(
            usuario=usuario,
            empresa=empresa,
            curso=curso,
            **serializer_data
        )
        
        return {'status_code': status.HTTP_201_CREATED}


@extend_schema(
    tags=['Perfis.Estagiario'],
    summary='Editar um estagiário',
    description='''
    Edita os dados de um estagiário existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - empresa_id: ID da empresa do estágio
    - curso_id: ID do curso
    - carga_horaria: Carga horária semanal
    - data_inicio_estagio: Data de início do estágio
    - data_fim_estagio: Data de fim do estágio
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=EstagiarioEditarSerializer,
    responses={
        status.HTTP_200_OK: {'description': 'Estagiário editado com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Estagiário não encontrado'},
    },
)
class EstagiarioEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de um estagiário existente.
    
    Apenas administradores podem editar estagiários.
    """
    serializer_class = EstagiarioEditarSerializer
    mensagem_sucesso = 'Estagiário editado com sucesso.'
    queryset = Estagiario.objects.all()
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context['instance'] = self.get_object()
        except Exception:
            pass
        return context

    def do_action_put(self, serializer_data, request):
        # Processa campos de FK se presentes
        dados_atualizacao = {}
        
        if 'empresa_id' in serializer_data:
            dados_atualizacao['empresa'] = Empresa.objects.get(pk=serializer_data.pop('empresa_id'))
        
        if 'curso_id' in serializer_data:
            dados_atualizacao['curso'] = Curso.objects.get(pk=serializer_data.pop('curso_id'))
        
        # Adiciona os demais campos
        dados_atualizacao.update(serializer_data)
        
        self.object.business.atualizar_dados(dados_atualizacao)


@extend_schema(
    tags=['Perfis.Estagiario'],
    summary='Deletar um estagiário',
    description='''
    Deleta um estagiário existente (soft delete - seta usuário.ativo=False).
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Observação:** Esta operação não remove o estagiário do banco de dados,
    apenas marca o usuário base como inativo (soft delete).
    ''',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Estagiário deletado com sucesso'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Estagiário não encontrado'},
    },
)
class EstagiarioDeletarView(IsAdminMixin, BasicDeleteAPIView):
    """
    View para deleção de um estagiário existente.
    
    Apenas administradores podem deletar estagiários.
    Realiza soft delete (seta usuário.ativo=False).
    """
    mensagem_sucesso = 'Estagiário deletado com sucesso.'
    queryset = Estagiario.objects.all()
    lookup_field = 'pk'

    def do_action_delete(self, request):
        self.object.business.deletar_dados()
