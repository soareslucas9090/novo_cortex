from drf_spectacular.utils import (
    extend_schema,
)

from AppCore.core.exceptions.exceptions import NotFoundException
from AppCore.basics.views.basic_views import BasicPostAPIView
from AppCore.basics.mixins.mixins import AllowAnyMixin
from Usuarios.usuario.models import Usuario

from .serializers import (
    EsqueceuSenhaSolicitarSerializer,
    ValidarCodigoEmailSerializer,
    EsqueceuSenhaConfirmarSerializer,
)


@extend_schema(tags=["Usuarios.Password reset"])
class SolicitarCodigoEsqueceuSenhaPostView(AllowAnyMixin, BasicPostAPIView):
    serializer_class = EsqueceuSenhaSolicitarSerializer
    mensagem_sucesso = "Código de verificação enviado para o email informado."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        
        try:
            usuario = Usuario.objects.get(contatos__email=email)
        except Usuario.MultipleObjectsReturned:
            usuario = Usuario.objects.filter(contatos__email=email).first()
        except NotFoundException:
            raise NotFoundException('Usuário com o email informado não encontrado.')
        
        codigo_redefinicao = usuario.conta_business.obter_codigo_redefinicao_senha(email)

        usuario.conta_business.enviar_email_redefinicao_senha(codigo_redefinicao, email)


@extend_schema(tags=["Usuarios.Password reset"])
class ValidarCodigoEmailPostView(AllowAnyMixin, BasicPostAPIView):
    serializer_class = ValidarCodigoEmailSerializer
    mensagem_sucesso = "Código validado com sucesso."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        codigo = serializer.get('codigo')
        
        try:
            usuario = Usuario.objects.get(contatos__email=email)
        except Usuario.MultipleObjectsReturned:
            usuario = Usuario.objects.filter(contatos__email=email).first()
        except NotFoundException:
            raise NotFoundException('Usuário com o email informado não encontrado.')
        
        usuario.conta_business.validar_codigo(codigo, email)


@extend_schema(tags=["Usuarios.Password reset"])
class RedefinirSenhaPostView(AllowAnyMixin, BasicPostAPIView):
    serializer_class = EsqueceuSenhaConfirmarSerializer
    mensagem_sucesso = "Senha redefinida com sucesso."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        codigo = serializer.get('codigo')
        nova_senha = serializer.get('nova_senha')
        
        try:
            usuario = Usuario.objects.get(contatos__email=email)
        except Usuario.MultipleObjectsReturned:
            usuario = Usuario.objects.filter(contatos__email=email).first()
        except NotFoundException:
            raise NotFoundException('Usuário com o email informado não encontrado.')
        
        usuario.conta_business.redefinir_senha(codigo, email, nova_senha)
