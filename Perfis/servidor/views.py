from drf_spectacular.utils import extend_schema

from rest_framework import status

from AppCore.basics.mixins.mixins import IsAdminMixin, IsOwnerOrAdminMixin
from AppCore.basics.views.basic_views import (
    BasicGetAPIView,
    BasicPostAPIView,
    BasicPutAPIView,
    BasicDeleteAPIView,
    BasicRetrieveAPIView,
)

from Perfis.servidor.models import Servidor
from Perfis.servidor.serializers import (
    ServidorListaSerializer,
    ServidorDetalheSerializer,
    ServidorCriarSerializer,
    ServidorEditarSerializer,
)

from Usuarios.usuario.models import Usuario


# ============================================================================
# VIEWS DE SERVIDOR
# ============================================================================

@extend_schema(
    tags=['Perfis.Servidor'],
    summary='Listar todos os servidores',
    description='''
    Retorna uma lista paginada de todos os servidores cadastrados no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - usuario_id, nome, cpf, tipo_servidor, jornada_trabalho
    - jornada_trabalho_display, classe, campus, ativo
    ''',
    responses={
        status.HTTP_200_OK: ServidorListaSerializer(many=True),
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class ServidorListaView(IsAdminMixin, BasicGetAPIView):
    """
    View para listagem de todos os servidores.
    
    Apenas administradores podem visualizar todos os servidores.
    Retorna uma lista resumida de todos os servidores cadastrados.
    """
    serializer_class = ServidorListaSerializer
    mensagem_sucesso = 'Servidores listados com sucesso.'

    def get_queryset(self):
        return Servidor.objects.select_related('usuario', 'usuario__campus').all()


@extend_schema(
    tags=['Perfis.Servidor'],
    summary='Visualizar detalhes de um servidor',
    description='''
    Retorna os dados completos de um servidor específico.
    
    **Permissões:** 
    - Administradores podem visualizar qualquer servidor
    - Usuários comuns podem visualizar apenas seu próprio perfil de servidor
    
    **Retorno:**
    - Dados completos do servidor incluindo dados funcionais
    - Informações do usuário base (contatos, endereços, setores)
    - Métricas calculadas (tempo de serviço)
    ''',
    responses={
        status.HTTP_200_OK: ServidorDetalheSerializer,
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão'},
        status.HTTP_404_NOT_FOUND: {'description': 'Servidor não encontrado'},
    },
)
class ServidorDetalheView(IsOwnerOrAdminMixin, BasicRetrieveAPIView):
    """
    View para visualização detalhada de um servidor.
    
    Administradores podem ver qualquer servidor.
    Usuários comuns podem ver apenas seu próprio perfil de servidor.
    """
    serializer_class = ServidorDetalheSerializer
    mensagem_sucesso = 'Servidor recuperado com sucesso.'
    queryset = Servidor.objects.select_related(
        'usuario',
        'usuario__campus'
    ).prefetch_related(
        'usuario__contatos',
        'usuario__enderecos',
        'usuario__usuario_setores',
        'usuario__usuario_setores__setor',
        'usuario__usuario_setores__campus',
    )
    lookup_field = 'pk'

    def obter_usuario_dono(self, obj):
        """Retorna o usuário dono do registro (para verificação de permissão)."""
        return obj.usuario


@extend_schema(
    tags=['Perfis.Servidor'],
    summary='Criar um novo servidor',
    description='''
    Cria um novo perfil de servidor para um usuário existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - usuario_id: ID do usuário base
    - data_posse: Data de posse do servidor
    - padrao: Padrão do servidor
    - classe: Classe do servidor
    - tipo_servidor: Tipo de servidor (Professor, Técnico, etc.)
    
    **Campos opcionais:**
    - jornada_trabalho: Jornada de trabalho (padrão: 40h)
    ''',
    request=ServidorCriarSerializer,
    responses={
        status.HTTP_201_CREATED: {'description': 'Servidor criado com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class ServidorCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de um novo servidor.
    
    Apenas administradores podem criar servidores.
    """
    serializer_class = ServidorCriarSerializer
    mensagem_sucesso = 'Servidor criado com sucesso.'

    def do_action_post(self, serializer_data, request):
        # Busca o usuário
        usuario = Usuario.objects.get(pk=serializer_data.pop('usuario_id'))
        
        # Cria o servidor
        Servidor.objects.create(usuario=usuario, **serializer_data)
        
        return {'status_code': status.HTTP_201_CREATED}


@extend_schema(
    tags=['Perfis.Servidor'],
    summary='Editar um servidor',
    description='''
    Edita os dados de um servidor existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - data_posse: Data de posse do servidor
    - jornada_trabalho: Jornada de trabalho
    - padrao: Padrão do servidor
    - classe: Classe do servidor
    - tipo_servidor: Tipo de servidor
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=ServidorEditarSerializer,
    responses={
        status.HTTP_200_OK: {'description': 'Servidor editado com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Servidor não encontrado'},
    },
)
class ServidorEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de um servidor existente.
    
    Apenas administradores podem editar servidores.
    """
    serializer_class = ServidorEditarSerializer
    mensagem_sucesso = 'Servidor editado com sucesso.'
    queryset = Servidor.objects.all()
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context['instance'] = self.get_object()
        except Exception:
            pass
        return context

    def do_action_put(self, serializer_data, request):
        self.object.business.atualizar_dados(serializer_data)


@extend_schema(
    tags=['Perfis.Servidor'],
    summary='Deletar um servidor',
    description='''
    Deleta um servidor existente (soft delete - seta usuário.ativo=False).
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Observação:** Esta operação não remove o servidor do banco de dados,
    apenas marca o usuário base como inativo (soft delete).
    ''',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Servidor deletado com sucesso'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Servidor não encontrado'},
    },
)
class ServidorDeletarView(IsAdminMixin, BasicDeleteAPIView):
    """
    View para deleção de um servidor existente.
    
    Apenas administradores podem deletar servidores.
    Realiza soft delete (seta usuário.ativo=False).
    """
    mensagem_sucesso = 'Servidor deletado com sucesso.'
    queryset = Servidor.objects.all()
    lookup_field = 'pk'

    def do_action_delete(self, request):
        self.object.business.deletar_dados()
