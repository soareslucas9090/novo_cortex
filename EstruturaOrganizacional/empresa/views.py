from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView, BasicPutAPIView

from EstruturaOrganizacional.empresa.models import Empresa
from EstruturaOrganizacional.empresa.serializers import (
    EmpresaListaSerializer,
    EmpresaCriarSerializer,
    EmpresaEditarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional.Empresa'],
    summary='Listar todas as empresas',
    description='''
    Retorna uma lista paginada de todas as empresas cadastradas no sistema.
    
    **Permissões:** Acesso público (não requer autenticação).
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, nome, cnpj, cnpj_formatado, is_active, total_terceirizados, total_estagiarios
    ''',
    responses={
        200: EmpresaListaSerializer(many=True),
    },
)
class EmpresaListaView(AllowAnyMixin, BasicGetAPIView):
    """
    View para listagem de todas as empresas.
    
    Acesso público - qualquer pessoa pode visualizar.
    Retorna uma lista resumida de todas as empresas cadastradas.
    """
    serializer_class = EmpresaListaSerializer
    mensagem_sucesso = 'Empresas listadas com sucesso.'

    def get_queryset(self):
        return Empresa.objects.prefetch_related('terceirizados', 'estagiarios').all()


@extend_schema(
    tags=['Estrutura Organizacional.Empresa'],
    summary='Criar uma nova empresa',
    description='''
    Cria uma nova empresa no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - nome: Nome da empresa
    - cnpj: CNPJ da empresa (14 dígitos, apenas números)
    
    **Campos opcionais:**
    - is_active: Se a empresa está ativa (padrão: True)
    ''',
    request=EmpresaCriarSerializer,
    responses={
        200: {'description': 'Empresa criada com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
    },
)
class EmpresaCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de uma nova empresa.
    
    Apenas administradores podem criar empresas.
    """
    serializer_class = EmpresaCriarSerializer
    mensagem_sucesso = 'Empresa criada com sucesso.'

    def do_action_post(self, serializer_data, request):
        Empresa.objects.create(**serializer_data)
        return {'status_code': 201}


@extend_schema(
    tags=['Estrutura Organizacional.Empresa'],
    summary='Editar uma empresa',
    description='''
    Edita os dados de uma empresa existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - nome: Nome da empresa
    - cnpj: CNPJ da empresa (14 dígitos, apenas números)
    - is_active: Se a empresa está ativa
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=EmpresaEditarSerializer,
    responses={
        200: {'description': 'Empresa editada com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
        404: {'description': 'Empresa não encontrada'},
    },
)
class EmpresaEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de uma empresa existente.
    
    Apenas administradores podem editar empresas.
    """
    serializer_class = EmpresaEditarSerializer
    mensagem_sucesso = 'Empresa editada com sucesso.'
    queryset = Empresa.objects.all()
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
