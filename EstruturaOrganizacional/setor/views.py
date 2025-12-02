from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView

from EstruturaOrganizacional.setor.models import Setor
from EstruturaOrganizacional.setor.serializers import (
    SetorListaSerializer,
    SetorCriarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional'],
    summary='Listar todos os setores',
    description='''
    Retorna uma lista paginada de todos os setores cadastrados no sistema.
    
    **Permissões:** Acesso público (não requer autenticação).
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, nome, is_active, total_membros
    ''',
    responses={
        200: SetorListaSerializer(many=True),
    },
)
class SetorListaView(AllowAnyMixin, BasicGetAPIView):
    """
    View para listagem de todos os setores.
    
    Acesso público - qualquer pessoa pode visualizar.
    Retorna uma lista resumida de todos os setores cadastrados.
    """
    serializer_class = SetorListaSerializer
    mensagem_sucesso = 'Setores listados com sucesso.'

    def get_queryset(self):
        return Setor.objects.prefetch_related('usuario_setores').all()


@extend_schema(
    tags=['Estrutura Organizacional'],
    summary='Criar um novo setor',
    description='''
    Cria um novo setor no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - nome: Nome do setor
    
    **Campos opcionais:**
    - is_active: Se o setor está ativo (padrão: True)
    ''',
    request=SetorCriarSerializer,
    responses={
        200: {'description': 'Setor criado com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
    },
)
class SetorCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de um novo setor.
    
    Apenas administradores podem criar setores.
    """
    serializer_class = SetorCriarSerializer
    mensagem_sucesso = 'Setor criado com sucesso.'

    def do_action_post(self, serializer_data, request):
        Setor.objects.create(**serializer_data)
        return {'status_code': 201}
