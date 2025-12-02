from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import AllowAnyMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicPostAPIView, BasicPutAPIView

from EstruturaOrganizacional.curso.models import Curso
from EstruturaOrganizacional.curso.serializers import (
    CursoListaSerializer,
    CursoCriarSerializer,
    CursoEditarSerializer,
)


@extend_schema(
    tags=['Estrutura Organizacional.Curso'],
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
    tags=['Estrutura Organizacional.Curso'],
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


@extend_schema(
    tags=['Estrutura Organizacional.Curso'],
    summary='Editar um curso',
    description='''
    Edita os dados de um curso existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - nome: Nome do curso
    - descricao: Descrição do curso
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=CursoEditarSerializer,
    responses={
        200: {'description': 'Curso editado com sucesso'},
        400: {'description': 'Dados inválidos'},
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
        404: {'description': 'Curso não encontrado'},
    },
)
class CursoEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de um curso existente.
    
    Apenas administradores podem editar cursos.
    """
    serializer_class = CursoEditarSerializer
    mensagem_sucesso = 'Curso editado com sucesso.'
    queryset = Curso.objects.all()
    lookup_field = 'pk'

    def do_action_put(self, instance, serializer_data, request):
        for attr, value in serializer_data.items():
            setattr(instance, attr, value)
        instance.save()
        return {}
