from drf_spectacular.utils import extend_schema

from AppCore.basics.views.basic_views import BasicGetAPIView
from AppCore.core.permissions.permissions import IsAdminPermission

from Usuarios.usuario.models import Usuario
from Usuarios.usuario.serializers import UsuarioListaSerializer


@extend_schema(
    tags=['Usuarios'],
    summary='Listar todos os usuários',
    description='''
    Retorna uma lista paginada de todos os usuários cadastrados no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - id, nome, cpf, campus, is_active, tipo_perfil
    ''',
    responses={
        200: UsuarioListaSerializer(many=True),
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão de administrador'},
    },
)
class UsuarioListaView(BasicGetAPIView):
    """
    View para listagem de todos os usuários.
    
    Apenas administradores podem acessar esta view.
    Retorna uma lista resumida de todos os usuários cadastrados.
    """
    permission_classes = [IsAdminPermission]
    serializer_class = UsuarioListaSerializer
    mensagem_sucesso = 'Usuários listados com sucesso.'

    def get_queryset(self):
        return Usuario.objects.select_related('campus').all()
