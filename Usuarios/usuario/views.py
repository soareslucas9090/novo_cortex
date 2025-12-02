from drf_spectacular.utils import extend_schema

from AppCore.basics.views.basic_views import BasicGetAPIView
from AppCore.core.permissions.permissions import IsAdminPermission

from Usuarios.usuario.models import Usuario
from Usuarios.usuario.serializers import UsuarioListaDetalhadaSerializer


@extend_schema(
    tags=['Usuarios'],
    summary='Listar todos os usuários',
    description='''
    Retorna uma lista paginada de todos os usuários cadastrados no sistema
    com informações detalhadas sobre seus setores, atividades e funções.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, nome, cpf, cpf_formatado, data_nascimento, data_ingresso
    - is_active, is_admin, campus, tipo_perfil
    - contatos (lista de emails e telefones)
    - setores (lista com detalhes de cada setor, incluindo atividades e funções)
    - total_setores_ativos
    ''',
    responses={
        200: UsuarioListaDetalhadaSerializer(many=True),
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
    },
)
class UsuarioListaView(BasicGetAPIView):
    """
    View para listagem de todos os usuários com informações detalhadas.
    
    Apenas administradores podem acessar esta view.
    Retorna uma lista detalhada de todos os usuários cadastrados,
    incluindo seus setores, atividades e funções.
    """
    permission_classes = [IsAdminPermission]
    serializer_class = UsuarioListaDetalhadaSerializer
    mensagem_sucesso = 'Usuários listados com sucesso.'

    def get_queryset(self):
        return Usuario.objects.select_related(
            'campus'
        ).prefetch_related(
            'contatos',
            'usuario_setores__setor__atividades__funcoes',
            'usuario_setores__campus',
        ).all()
