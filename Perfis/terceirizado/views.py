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

from Perfis.terceirizado.models import Terceirizado
from Perfis.terceirizado.serializers import (
    TerceirizadoListaSerializer,
    TerceirizadoDetalheSerializer,
    TerceirizadoCriarSerializer,
    TerceirizadoEditarSerializer,
)

from Usuarios.usuario.models import Usuario
from EstruturaOrganizacional.empresa.models import Empresa


# ============================================================================
# VIEWS DE TERCEIRIZADO
# ============================================================================

@extend_schema(
    tags=['Perfis.Terceirizado'],
    summary='Listar todos os terceirizados',
    description='''
    Retorna uma lista paginada de todos os terceirizados cadastrados no sistema.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Paginação:**
    - Padrão: 10 itens por página
    - Use o query param `paginacao` para alterar (entre 1 e 100)
    
    **Retorno:**
    - usuario_id, nome, cpf, empresa, data_inicio_contrato
    - data_fim_contrato, campus, ativo, contrato_ativo
    ''',
    responses={
        status.HTTP_200_OK: TerceirizadoListaSerializer(many=True),
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class TerceirizadoListaView(IsAdminMixin, BasicGetAPIView):
    """
    View para listagem de todos os terceirizados.
    
    Apenas administradores podem visualizar todos os terceirizados.
    Retorna uma lista resumida de todos os terceirizados cadastrados.
    """
    serializer_class = TerceirizadoListaSerializer
    mensagem_sucesso = 'Terceirizados listados com sucesso.'

    def get_queryset(self):
        return Terceirizado.objects.select_related(
            'usuario',
            'usuario__campus',
            'empresa'
        ).all()


@extend_schema(
    tags=['Perfis.Terceirizado'],
    summary='Visualizar detalhes de um terceirizado',
    description='''
    Retorna os dados completos de um terceirizado específico.
    
    **Permissões:** 
    - Administradores podem visualizar qualquer terceirizado
    - Usuários comuns podem visualizar apenas seu próprio perfil de terceirizado
    
    **Retorno:**
    - Dados completos do terceirizado incluindo empresa
    - Informações do usuário base (contatos, endereços, setores)
    - Métricas calculadas do contrato
    ''',
    responses={
        status.HTTP_200_OK: TerceirizadoDetalheSerializer,
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão'},
        status.HTTP_404_NOT_FOUND: {'description': 'Terceirizado não encontrado'},
    },
)
class TerceirizadoDetalheView(IsOwnerOrAdminMixin, BasicRetrieveAPIView):
    """
    View para visualização detalhada de um terceirizado.
    
    Administradores podem ver qualquer terceirizado.
    Usuários comuns podem ver apenas seu próprio perfil de terceirizado.
    """
    serializer_class = TerceirizadoDetalheSerializer
    mensagem_sucesso = 'Terceirizado recuperado com sucesso.'
    queryset = Terceirizado.objects.select_related(
        'usuario',
        'usuario__campus',
        'empresa'
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
    tags=['Perfis.Terceirizado'],
    summary='Criar um novo terceirizado',
    description='''
    Cria um novo perfil de terceirizado para um usuário existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos obrigatórios:**
    - usuario_id: ID do usuário base
    - empresa_id: ID da empresa
    - data_inicio_contrato: Data de início do contrato
    
    **Campos opcionais:**
    - data_fim_contrato: Data de fim do contrato
    ''',
    request=TerceirizadoCriarSerializer,
    responses={
        status.HTTP_201_CREATED: {'description': 'Terceirizado criado com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
    },
)
class TerceirizadoCriarView(IsAdminMixin, BasicPostAPIView):
    """
    View para criação de um novo terceirizado.
    
    Apenas administradores podem criar terceirizados.
    """
    serializer_class = TerceirizadoCriarSerializer
    mensagem_sucesso = 'Terceirizado criado com sucesso.'

    def do_action_post(self, serializer_data, request):
        # Busca as entidades relacionadas
        usuario = Usuario.objects.get(pk=serializer_data.pop('usuario_id'))
        empresa = Empresa.objects.get(pk=serializer_data.pop('empresa_id'))
        
        # Cria o terceirizado
        Terceirizado.objects.create(
            usuario=usuario,
            empresa=empresa,
            **serializer_data
        )
        
        return {'status_code': status.HTTP_201_CREATED}


@extend_schema(
    tags=['Perfis.Terceirizado'],
    summary='Editar um terceirizado',
    description='''
    Edita os dados de um terceirizado existente.
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Campos editáveis (todos opcionais):**
    - empresa_id: ID da empresa
    - data_inicio_contrato: Data de início do contrato
    - data_fim_contrato: Data de fim do contrato
    
    **Observação:** Apenas envie os campos que deseja alterar.
    ''',
    request=TerceirizadoEditarSerializer,
    responses={
        status.HTTP_200_OK: {'description': 'Terceirizado editado com sucesso'},
        status.HTTP_400_BAD_REQUEST: {'description': 'Dados inválidos'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Terceirizado não encontrado'},
    },
)
class TerceirizadoEditarView(IsAdminMixin, BasicPutAPIView):
    """
    View para edição de um terceirizado existente.
    
    Apenas administradores podem editar terceirizados.
    """
    serializer_class = TerceirizadoEditarSerializer
    mensagem_sucesso = 'Terceirizado editado com sucesso.'
    queryset = Terceirizado.objects.all()
    lookup_field = 'pk'

    def get_serializer_context(self):
        context = super().get_serializer_context()
        try:
            context['instance'] = self.get_object()
        except Exception:
            pass
        return context

    def do_action_put(self, serializer_data, request):
        # Processa campos de FK se presentes
        dados_atualizacao = {}
        
        if 'empresa_id' in serializer_data:
            dados_atualizacao['empresa'] = Empresa.objects.get(pk=serializer_data.pop('empresa_id'))
        
        # Adiciona os demais campos
        dados_atualizacao.update(serializer_data)
        
        self.object.business.atualizar_dados(dados_atualizacao)


@extend_schema(
    tags=['Perfis.Terceirizado'],
    summary='Deletar um terceirizado',
    description='''
    Deleta um terceirizado existente (soft delete - seta usuário.ativo=False).
    
    **Permissões:** Apenas administradores (is_admin ou is_superuser) podem acessar.
    
    **Observação:** Esta operação não remove o terceirizado do banco de dados,
    apenas marca o usuário base como inativo (soft delete).
    ''',
    responses={
        status.HTTP_204_NO_CONTENT: {'description': 'Terceirizado deletado com sucesso'},
        status.HTTP_401_UNAUTHORIZED: {'description': 'Não autenticado'},
        status.HTTP_403_FORBIDDEN: {'description': 'Sem permissão de administrador'},
        status.HTTP_404_NOT_FOUND: {'description': 'Terceirizado não encontrado'},
    },
)
class TerceirizadoDeletarView(IsAdminMixin, BasicDeleteAPIView):
    """
    View para deleção de um terceirizado existente.
    
    Apenas administradores podem deletar terceirizados.
    Realiza soft delete (seta usuário.ativo=False).
    """
    mensagem_sucesso = 'Terceirizado deletado com sucesso.'
    queryset = Terceirizado.objects.all()
    lookup_field = 'pk'

    def do_action_delete(self, request):
        self.object.business.deletar_dados()
