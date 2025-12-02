from drf_spectacular.utils import extend_schema

from AppCore.basics.mixins.mixins import IsOwnerOrAdminMixin, IsAdminMixin
from AppCore.basics.views.basic_views import BasicGetAPIView, BasicRetrieveAPIView

from Usuarios.usuario.models import Usuario
from Usuarios.usuario.serializers import UsuarioListaDetalhadaSerializer, UsuarioCompletoSerializer


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
class UsuarioListaView(IsAdminMixin, BasicGetAPIView):
    """
    View para listagem de todos os usuários com informações detalhadas.
    
    Apenas administradores podem acessar esta view.
    Retorna uma lista detalhada de todos os usuários cadastrados,
    incluindo seus setores, atividades e funções.
    """
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


@extend_schema(
    tags=['Usuarios'],
    summary='Recuperar dados de um usuário específico',
    description='''
    Retorna os dados completos de um usuário específico.
    
    **Permissões:** 
    - O próprio usuário pode acessar seus dados
    - Administradores (is_admin ou is_superuser) podem acessar dados de qualquer usuário
    
    **Retorno:**
    - Dados básicos: id, nome, cpf, cpf_formatado, data_nascimento, data_ingresso
    - Status: is_active, is_admin, is_staff, is_superuser, last_login
    - Relacionamentos: campus, tipo_perfil
    - Contatos completos (email, telefone, timestamps)
    - Endereços completos (logradouro, bairro, cidade, estado, cep, etc)
    - Setores vinculados com atividades e funções
    - Perfis: servidor, aluno, terceirizado, estagiário (se existirem)
    ''',
    responses={
        200: UsuarioCompletoSerializer,
        401: {'description': 'Não autenticado'},
        403: {'description': 'Sem permissão para acessar este recurso'},
        404: {'description': 'Usuário não encontrado'},
    },
)
class UsuarioRetrieveView(IsOwnerOrAdminMixin, BasicRetrieveAPIView):
    """
    View para recuperar dados de um usuário específico.
    
    O próprio usuário ou administradores podem acessar.
    Retorna os dados completos do usuário, incluindo contatos,
    endereços, setores, atividades e perfis.
    """
    serializer_class = UsuarioCompletoSerializer
    mensagem_sucesso = 'Usuário recuperado com sucesso.'
    lookup_field = 'pk'

    def get_queryset(self):
        return Usuario.objects.select_related(
            'campus', 'cargo'
        ).prefetch_related(
            'contatos',
            'enderecos',
            'usuario_setores__setor__atividades__funcoes',
            'usuario_setores__campus',
        ).all()

    def obter_usuario_dono(self, obj):
        """
        Retorna o usuário dono do objeto.
        
        Como o objeto é o próprio usuário, retorna ele mesmo.
        """
        return obj
