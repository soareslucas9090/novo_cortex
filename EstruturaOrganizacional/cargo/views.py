from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView, BasicPutAPIView

from EstruturaOrganizacional.cargo.models import Cargo
from EstruturaOrganizacional.cargo.serializers import (
    CargoListaSerializer,
    CargoCriarSerializer,
    CargoEditarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional.Cargo'],
    summary='Listar todos os cargos',
    description='''
    Retorna uma lista paginada de todos os cargos cadastrados no sistema.
    
    **Permissões:** Acesso público (não requer autenticação).
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, descricao
    ''',
    responses={
        200: CargoListaSerializer(many=True),
    },
)
class CargoListaView(AllowAnyMixin, BasicGetAPIView):
    """
    View para listagem de todos os cargos.
    
    Acesso público - qualquer pessoa pode visualizar.
    Retorna uma lista de todos os cargos cadastrados.
    """
    serializer_class = CargoListaSerializer
    mensagem_sucesso = 'Cargos listados com sucesso.'

    def get_queryset(self):
        return Cargo.objects.all()


@extend_schema(
    tags=['Estrutura Organizacional.Cargo'],
    summary='Criar um novo cargo',
    description='''
    Cria um novo cargo no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - descricao: Descrição do cargo
    ''',
    request=CargoCriarSerializer,
    responses={
        201: {'description': 'Cargo criado com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
    },
)
class CargoCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de um novo cargo.
    
    Apenas administradores podem criar cargos.
    """
    serializer_class = CargoCriarSerializer
    mensagem_sucesso = 'Cargo criado com sucesso.'

    def do_action_post(self, serializer_data, request):
        Cargo.objects.create(**serializer_data)
        return {'status_code': 201}


@extend_schema(
    tags=['Estrutura Organizacional.Cargo'],
    summary='Editar um cargo',
    description='''
    Edita os dados de um cargo existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - descricao: Descrição do cargo
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=CargoEditarSerializer,
    responses={
        200: {'description': 'Cargo editado com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
        404: {'description': 'Cargo não encontrado'},
    },
)
class CargoEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de um cargo existente.
    
    Apenas administradores podem editar cargos.
    """
    serializer_class = CargoEditarSerializer
    mensagem_sucesso = 'Cargo editado com sucesso.'
    queryset = Cargo.objects.all()
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
