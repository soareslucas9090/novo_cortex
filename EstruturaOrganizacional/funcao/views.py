from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView

from EstruturaOrganizacional.funcao.models import Funcao
from EstruturaOrganizacional.funcao.serializers import (
    FuncaoListaSerializer,
    FuncaoCriarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional - Função'],
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
        200: FuncaoListaSerializer(many=True),
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
    tags=['Estrutura Organizacional - Função'],
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
        200: {'description': 'Função criada com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
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
        return {'status_code': 201}
