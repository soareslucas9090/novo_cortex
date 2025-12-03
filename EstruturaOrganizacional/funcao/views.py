from drf_spectacular.utils import extend_schema

from rest_framework import status

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView, BasicPutAPIView

from EstruturaOrganizacional.funcao.models import Funcao
from EstruturaOrganizacional.funcao.serializers import (
    FuncaoListaSerializer,
    FuncaoCriarSerializer,
    FuncaoEditarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional.Função'],
    summary='Listar todas as funções',
    description='''
    Retorna uma lista paginada de todas as funções cadastradas no sistema.
    
    **Permissões:** Acesso público (não requer autenticação).
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, descricao, descricao_resumida, atividade, setor_nome
    ''',
    responses={
        status.HTTP_200_OK: FuncaoListaSerializer(many=True),
    },
)
class FuncaoListaView(AllowAnyMixin, BasicGetAPIView):
    """
    View para listagem de todas as funções.
    
    Acesso público - qualquer pessoa pode visualizar.
    Retorna uma lista resumida de todas as funções cadastradas.
    """
    serializer_class = FuncaoListaSerializer
    mensagem_sucesso = 'Funções listadas com sucesso.'

    def get_queryset(self):
        return Funcao.objects.select_related('atividade', 'atividade__setor').all()


@extend_schema(
    tags=['Estrutura Organizacional.Função'],
    summary='Criar uma nova função',
    description='''
    Cria uma nova função no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - atividade_id: ID da atividade à qual a função pertence
    - descricao: Descrição da função
    ''',
    request=FuncaoCriarSerializer,
    responses={
        status.HTTP_200_OK: {'description': 'Função criada com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class FuncaoCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de uma nova função.
    
    Apenas administradores podem criar funções.
    """
    serializer_class = FuncaoCriarSerializer
    mensagem_sucesso = 'Função criada com sucesso.'

    def do_action_post(self, serializer_data, request):
        atividade = serializer_data.pop('atividade')
        Funcao.objects.create(atividade=atividade, **serializer_data)
        return {'status_code': status.HTTP_201_CREATED}


@extend_schema(
    tags=['Estrutura Organizacional.Função'],
    summary='Editar uma função',
    description='''
    Edita os dados de uma função existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - atividade_id: ID da atividade à qual a função pertence
    - descricao: Descrição da função
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=FuncaoEditarSerializer,
    responses={
        status.HTTP_200_OK: {'description': 'Função editada com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Função não encontrada'},
    },
)
class FuncaoEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de uma função existente.
    
    Apenas administradores podem editar funções.
    """
    serializer_class = FuncaoEditarSerializer
    mensagem_sucesso = 'Função editada com sucesso.'
    queryset = Funcao.objects.all()
    lookup_field = 'pk'

    def do_action_put(self, serializer_data, request):
        self.object.business.atualizar_dados(serializer_data)
