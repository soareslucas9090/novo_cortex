from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView, BasicPutAPIView

from EstruturaOrganizacional.setor.models import Setor
from EstruturaOrganizacional.setor.serializers import (
    SetorListaSerializer,
    SetorCriarSerializer,
    SetorEditarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional.Setor'],
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
    tags=['Estrutura Organizacional.Setor'],
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


@extend_schema(
    tags=['Estrutura Organizacional.Setor'],
    summary='Editar um setor',
    description='''
    Edita os dados de um setor existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - nome: Nome do setor
    - is_active: Se o setor está ativo
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=SetorEditarSerializer,
    responses={
        200: {'description': 'Setor editado com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
        404: {'description': 'Setor não encontrado'},
    },
)
class SetorEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de um setor existente.
    
    Apenas administradores podem editar setores.
    """
    serializer_class = SetorEditarSerializer
    mensagem_sucesso = 'Setor editado com sucesso.'
    queryset = Setor.objects.all()
    lookup_field = 'pk'

    def do_action_put(self, instance, serializer_data, request):
        for attr, value in serializer_data.items():
            setattr(instance, attr, value)
        instance.save()
        return {}
