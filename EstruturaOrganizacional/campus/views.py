from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView, BasicPutAPIView

from EstruturaOrganizacional.campus.models import Campus
from EstruturaOrganizacional.campus.serializers import (
    CampusListaSerializer,
    CampusCriarSerializer,
    CampusEditarSerializer,
)


# ============================================================================
# VIEWS DE CAMPUS
# ============================================================================

@extend_schema(
    tags=['Estrutura Organizacional'],
    summary='Listar todos os campi',
    description='''
    Retorna uma lista paginada de todos os campi cadastrados no sistema.
    
    **Permissões:** Acesso público (não requer autenticação).
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, nome, cnpj, cnpj_formatado, is_active
    ''',
    responses={
        200: CampusListaSerializer(many=True),
    },
)
class CampusListaView(AllowAnyMixin, BasicGetAPIView):
    """
    View para listagem de todos os campi.
    
    Acesso público - qualquer pessoa pode visualizar.
    Retorna uma lista resumida de todos os campi cadastrados.
    """
    serializer_class = CampusListaSerializer
    mensagem_sucesso = 'Campi listados com sucesso.'

    def get_queryset(self):
        return Campus.objects.all()


@extend_schema(
    tags=['Estrutura Organizacional'],
    summary='Criar um novo campus',
    description='''
    Cria um novo campus no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - nome: Nome do campus
    - cnpj: CNPJ do campus (14 dígitos, apenas números)
    
    **Campos opcionais:**
    - is_active: Se o campus está ativo (padrão: True)
    ''',
    request=CampusCriarSerializer,
    responses={
        200: {'description': 'Campus criado com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
    },
)
class CampusCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de um novo campus.
    
    Apenas administradores podem criar campi.
    """
    serializer_class = CampusCriarSerializer
    mensagem_sucesso = 'Campus criado com sucesso.'

    def do_action_post(self, serializer_data, request):
        Campus.objects.create(**serializer_data)
        return {'status_code': 201}


@extend_schema(
    tags=['Estrutura Organizacional'],
    summary='Editar um campus',
    description='''
    Edita os dados de um campus existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - nome: Nome do campus
    - cnpj: CNPJ do campus (14 dígitos, apenas números)
    - is_active: Se o campus está ativo
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=CampusEditarSerializer,
    responses={
        200: {'description': 'Campus editado com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
        404: {'description': 'Campus não encontrado'},
    },
)
class CampusEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de um campus existente.
    
    Apenas administradores podem editar campi.
    """
    serializer_class = CampusEditarSerializer
    mensagem_sucesso = 'Campus editado com sucesso.'
    queryset = Campus.objects.all()
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context['instance'] = self.get_object()
        except Exception:
            pass
        return context

    def do_action_put(self, instance, serializer_data, request):
        for attr, value in serializer_data.items():
            setattr(instance, attr, value)
        instance.save()
        return {}
