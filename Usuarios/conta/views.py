from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import AllowAny

from AppCore.core.exceptions.exceptions import NotFoundException
from AppCore.basics.views.basic_views import BasicPostAPIView
from AppCore.basics.mixins.mixins import AllowAnyMixin
from Usuarios.usuario.models import Usuario

from .serializers import (
    CriarContaSerializer, ConfirmarCodigoCriarContaSerializer,
    ConfirmarSenhaCriarContaSerializer, EsqueceuSenhaSolicitarSerializer,
    EsqueceuSenhaConfirmarSerializer
)
from .business import ContaBusiness


@extend_schema(tags=["Usuarios.Create conta"])
class CriarContaPostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = CriarContaSerializer
    mensagem_sucesso = "Código de verificação enviado para o email informado."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        tipo_perfil = serializer.get('tipo_perfil')
        
        conta_business = ContaBusiness()

        codigo_email_conta = conta_business.obter_codigo(email, tipo_perfil)

        conta_business.enviar_email_verificacao(email, codigo_email_conta)


@extend_schema(tags=["Usuarios.Create conta"])       
class ConfirmarCodigoCriarContaPostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = ConfirmarCodigoCriarContaSerializer
    mensagem_sucesso = "Código verificado. Você pode prosseguir com a criação da conta."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        codigo = serializer.get('codigo')
        
        conta_business = ContaBusiness()
        
        conta_business.validar_codigo(email=email, codigo=codigo)

        
@extend_schema(tags=["Usuarios.Create conta"])
class ConfirmarSenhaContaPostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = ConfirmarSenhaCriarContaSerializer
    mensagem_sucesso = "Usuário criado com sucesso."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        codigo = serializer.get('codigo')
        senha = serializer.get('senha')
        telefone = serializer.get('telefone')
        data_nascimento = serializer.get('data_nascimento')
        tipo_perfil = serializer.get('tipo_perfil')
        bio = serializer.get('bio')
        nome = serializer.get('nome')
        
        conta_business = ContaBusiness()
        conta_business.criar_conta_usuario(
            email, codigo, nome, senha, telefone, data_nascimento, tipo_perfil, bio
        )
        
        return {
            'message': 'Usuário criado com sucesso.',
            'status_code': status.HTTP_201_CREATED
        }


@extend_schema(tags=["Usuarios.Password reset"])
class SolicitarCodigoEsqueceuSenhaPostView(AllowAnyMixin, BasicPostAPIView):
    serializer_class = EsqueceuSenhaSolicitarSerializer
    mensagem_sucesso = "Código de verificação enviado para o email informado."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        
        try:
            usuario = Usuario.objects.get(email=email)
        except NotFoundException:
            raise NotFoundException('Usuário com o email informado não encontrado.')
        
        codigo_redefinicao = usuario.conta_business.obter_codigo_redefinicao_senha()

        usuario.conta_business.enviar_email_redefinicao_senha(codigo_redefinicao)
