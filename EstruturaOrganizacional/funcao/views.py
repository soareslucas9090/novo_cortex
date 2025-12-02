from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView, BasicPutAPIView

from EstruturaOrganizacional.funcao.models import Funcao
from EstruturaOrganizacional.funcao.serializers import (
    FuncaoListaSerializer,
    FuncaoCriarSerializer,
    FuncaoEditarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional'],
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
    tags=['Estrutura Organizacional'],
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


@extend_schema(
    tags=['Estrutura Organizacional'],
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
        200: {'description': 'Função editada com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
        404: {'description': 'Função não encontrada'},
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

    def do_action_put(self, instance, serializer_data, request):
        for attr, value in serializer_data.items():
            setattr(instance, attr, value)
        instance.save()
        return {}
