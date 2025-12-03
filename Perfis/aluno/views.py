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

from Perfis.aluno.models import Aluno
from Perfis.aluno.serializers import (
    AlunoListaSerializer,
    AlunoDetalheSerializer,
    AlunoCriarSerializer,
    AlunoEditarSerializer,
)

from Usuarios.usuario.models import Usuario


# ============================================================================
# VIEWS DE ALUNO
# ============================================================================

@extend_schema(
    tags=['Perfis.Aluno'],
    summary='Listar todos os alunos',
    description='''
    Retorna uma lista paginada de todos os alunos cadastrados no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - usuario_id, nome, cpf, ira, turno, turno_display, previsao_conclusao
    - aluno_especial, campus, ativo, is_formado
    ''',
    responses={
        status.HTTP_200_OK: AlunoListaSerializer(many=True),
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class AlunoListaView(IsAdminMixin, BasicGetAPIView):
    """
    View para listagem de todos os alunos.
    
    Apenas administradores podem visualizar todos os alunos.
    Retorna uma lista resumida de todos os alunos cadastrados.
    """
    serializer_class = AlunoListaSerializer
    mensagem_sucesso = 'Alunos listados com sucesso.'

    def get_queryset(self):
        return Aluno.objects.select_related('usuario', 'usuario__campus').all()


@extend_schema(
    tags=['Perfis.Aluno'],
    summary='Visualizar detalhes de um aluno',
    description='''
    Retorna os dados completos de um aluno específico.
    
    **Permissões:** 
    - Administradores podem visualizar qualquer aluno
    - Usuários comuns podem visualizar apenas seu próprio perfil de aluno
    
    **Retorno:**
    - Dados completos do aluno incluindo dados acadêmicos
    - Informações do usuário base (contatos, endereços, setores)
    - Métricas calculadas
    ''',
    responses={
        status.HTTP_200_OK: AlunoDetalheSerializer,
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão'},
        status.HTTP_404_NOT_FOUND: {'description': 'Aluno não encontrado'},
    },
)
class AlunoDetalheView(IsOwnerOrAdminMixin, BasicRetrieveAPIView):
    """
    View para visualização detalhada de um aluno.
    
    Administradores podem ver qualquer aluno.
    Usuários comuns podem ver apenas seu próprio perfil de aluno.
    """
    serializer_class = AlunoDetalheSerializer
    mensagem_sucesso = 'Aluno recuperado com sucesso.'
    queryset = Aluno.objects.select_related(
        'usuario',
        'usuario__campus'
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
    tags=['Perfis.Aluno'],
    summary='Criar um novo aluno',
    description='''
    Cria um novo perfil de aluno para um usuário existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - usuario_id: ID do usuário base
    - previsao_conclusao: Ano previsto para conclusão do curso
    
    **Campos opcionais:**
    - ira: Índice de Rendimento Acadêmico (padrão: 0.00)
    - forma_ingresso: Forma de ingresso (padrão: ENEM)
    - aluno_especial: Se é aluno especial (padrão: False)
    - turno: Turno do aluno (padrão: Integral)
    - ativo: Se o aluno está ativo (padrão: True)
    ''',
    request=AlunoCriarSerializer,
    responses={
        status.HTTP_201_CREATED: {'description': 'Aluno criado com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class AlunoCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de um novo aluno.
    
    Apenas administradores podem criar alunos.
    """
    serializer_class = AlunoCriarSerializer
    mensagem_sucesso = 'Aluno criado com sucesso.'

    def do_action_post(self, serializer_data, request):
        # Busca o usuário
        usuario = Usuario.objects.get(pk=serializer_data.pop('usuario_id'))
        
        # Cria o aluno
        Aluno.objects.create(usuario=usuario, **serializer_data)
        
        return {'status_code': status.HTTP_201_CREATED}


@extend_schema(
    tags=['Perfis.Aluno'],
    summary='Editar um aluno',
    description='''
    Edita os dados de um aluno existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - ira: Índice de Rendimento Acadêmico
    - forma_ingresso: Forma de ingresso
    - previsao_conclusao: Ano previsto para conclusão
    - aluno_especial: Se é aluno especial
    - turno: Turno do aluno
    - ativo: Se o aluno está ativo
    - ano_conclusao: Ano de conclusão (para formados)
    - data_colacao: Data de colação (para formados)
    - data_expedicao_diploma: Data de expedição do diploma (para formados)
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=AlunoEditarSerializer,
    responses={
        status.HTTP_200_OK: {'description': 'Aluno editado com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Aluno não encontrado'},
    },
)
class AlunoEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de um aluno existente.
    
    Apenas administradores podem editar alunos.
    """
    serializer_class = AlunoEditarSerializer
    mensagem_sucesso = 'Aluno editado com sucesso.'
    queryset = Aluno.objects.all()
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context['instance'] = self.get_object()
        except Exception:
            pass
        return context

    def do_action_put(self, serializer_data, request):
        self.object.business.atualizar_dados(serializer_data)


@extend_schema(
    tags=['Perfis.Aluno'],
    summary='Deletar um aluno',
    description='''
    Deleta um aluno existente (soft delete - seta ativo=False).
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Observação:** Esta operação não remove o aluno do banco de dados,
    apenas marca como inativo (soft delete).
    ''',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Aluno deletado com sucesso'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Aluno não encontrado'},
    },
)
class AlunoDeletarView(IsAdminMixin, BasicDeleteAPIView):
    """
    View para deleção de um aluno existente.
    
    Apenas administradores podem deletar alunos.
    Realiza soft delete (seta ativo=False).
    """
    mensagem_sucesso = 'Aluno deletado com sucesso.'
    queryset = Aluno.objects.all()
    lookup_field = 'pk'

    def do_action_delete(self, request):
        self.object.business.deletar_dados()
