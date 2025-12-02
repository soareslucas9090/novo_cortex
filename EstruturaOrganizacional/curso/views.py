from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView

from EstruturaOrganizacional.curso.models import Curso
from EstruturaOrganizacional.curso.serializers import (
    CursoListaSerializer,
    CursoCriarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional - Curso'],
    summary='Listar todos os cursos',
    description='''
    Retorna uma lista paginada de todos os cursos cadastrados no sistema.
    
    **Permissões:** Acesso público (não requer autenticação).
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, nome, descricao, descricao_resumida, total_estagiarios
    ''',
    responses={
        200: CursoListaSerializer(many=True),
    },
)
class CursoListaView(AllowAnyMixin, BasicGetAPIView):
    """
    View para listagem de todos os cursos.
    
    Acesso público - qualquer pessoa pode visualizar.
    Retorna uma lista resumida de todos os cursos cadastrados.
    """
    serializer_class = CursoListaSerializer
    mensagem_sucesso = 'Cursos listados com sucesso.'

    def get_queryset(self):
        return Curso.objects.prefetch_related('estagiarios').all()


@extend_schema(
    tags=['Estrutura Organizacional - Curso'],
    summary='Criar um novo curso',
    description='''
    Cria um novo curso no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - nome: Nome do curso
    
    **Campos opcionais:**
    - descricao: Descrição do curso
    ''',
    request=CursoCriarSerializer,
    responses={
        200: {'description': 'Curso criado com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
    },
)
class CursoCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de um novo curso.
    
    Apenas administradores podem criar cursos.
    """
    serializer_class = CursoCriarSerializer
    mensagem_sucesso = 'Curso criado com sucesso.'

    def do_action_post(self, serializer_data, request):
        Curso.objects.create(**serializer_data)
        return {'status_code': 201}
