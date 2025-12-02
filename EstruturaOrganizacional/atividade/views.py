from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView

from EstruturaOrganizacional.atividade.models import Atividade
from EstruturaOrganizacional.atividade.serializers import (
    AtividadeListaSerializer,
    AtividadeCriarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional - Atividade'],
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
        200: AtividadeListaSerializer(many=True),
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
    tags=['Estrutura Organizacional - Atividade'],
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
        200: {'description': 'Atividade criada com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
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
        return {'status_code': 201}
