from drf_spectacular.utils import extend_schema

from rest_framework import status

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView, BasicPutAPIView, BasicDeleteAPIView

from EstruturaOrganizacional.atividade.models import Atividade
from EstruturaOrganizacional.atividade.serializers import (
    AtividadeListaSerializer,
    AtividadeCriarSerializer,
    AtividadeEditarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional.Atividade'],
    summary='Listar todas as atividades',
    description='''
    Retorna uma lista paginada de todas as atividades cadastradas no sistema.
    
    **Permissões:** Acesso público (não requer autenticação).
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, descricao, descricao_resumida, setor, total_funcoes
    ''',
    responses={
        status.HTTP_200_OK: AtividadeListaSerializer(many=True),
    },
)
class AtividadeListaView(AllowAnyMixin, BasicGetAPIView):
    """
    View para listagem de todas as atividades.
    
    Acesso público - qualquer pessoa pode visualizar.
    Retorna uma lista resumida de todas as atividades cadastradas.
    """
    serializer_class = AtividadeListaSerializer
    mensagem_sucesso = 'Atividades listadas com sucesso.'

    def get_queryset(self):
        return Atividade.objects.select_related('setor').prefetch_related('funcoes').all()


@extend_schema(
    tags=['Estrutura Organizacional.Atividade'],
    summary='Criar uma nova atividade',
    description='''
    Cria uma nova atividade no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - setor_id: ID do setor ao qual a atividade pertence
    - descricao: Descrição da atividade
    ''',
    request=AtividadeCriarSerializer,
    responses={
        status.HTTP_200_OK: {'description': 'Atividade criada com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class AtividadeCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de uma nova atividade.
    
    Apenas administradores podem criar atividades.
    """
    serializer_class = AtividadeCriarSerializer
    mensagem_sucesso = 'Atividade criada com sucesso.'

    def do_action_post(self, serializer_data, request):
        setor = serializer_data.pop('setor')
        Atividade.objects.create(setor=setor, **serializer_data)
        return {'status_code': status.HTTP_201_CREATED}


@extend_schema(
    tags=['Estrutura Organizacional.Atividade'],
    summary='Editar uma atividade',
    description='''
    Edita os dados de uma atividade existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - setor_id: ID do setor ao qual a atividade pertence
    - descricao: Descrição da atividade
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=AtividadeEditarSerializer,
    responses={
        status.HTTP_200_OK: {'description': 'Atividade editada com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Atividade não encontrada'},
    },
)
class AtividadeEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de uma atividade existente.
    
    Apenas administradores podem editar atividades.
    """
    serializer_class = AtividadeEditarSerializer
    mensagem_sucesso = 'Atividade editada com sucesso.'
    queryset = Atividade.objects.all()
    lookup_field = 'pk'

    def do_action_put(self, serializer_data, request):
        self.object.business.atualizar_dados(serializer_data)


@extend_schema(
    tags=['Estrutura Organizacional.Atividade'],
    summary='Deletar uma atividade',
    description='''
    Deleta uma atividade existente do sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Observação:** Esta operação remove permanentemente a atividade do banco de dados.
    ''',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Atividade deletada com sucesso'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Atividade não encontrada'},
    },
)
class AtividadeDeletarView(IsAdminMixin, BasicDeleteAPIView):
    """
    View para deleção de uma atividade existente.
    
    Apenas administradores podem deletar atividades.
    """
    mensagem_sucesso = 'Atividade deletada com sucesso.'
    queryset = Atividade.objects.all()
    lookup_field = 'pk'

    def do_action_delete(self, request):
        self.object.business.deletar_dados()
