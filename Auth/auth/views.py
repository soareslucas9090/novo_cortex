from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from .serializers import LoginSerializer, LoginInputSerializer, LoginResponseSerializer


@extend_schema(
    tags=['Auth'],
    summary='Login via CPF',
    description='''
    Realiza o login do usuário utilizando CPF e senha.
    
    Retorna:
    - **access**: Token de acesso JWT (válido por 30 minutos)
    - **refresh**: Token de refresh JWT (válido por 7 dias)
    - **usuario**: Dados básicos do usuário (id, nome, cpf, permissões)
    - **campus**: Campus vinculado ao usuário
    - **perfis**: Lista de perfis (Servidor, Aluno, Terceirizado, Estagiário)
    - **setores**: Setores ativos com atividades e funções
    - **permissoes**: Flags de permissões administrativas
    ''',
    request=LoginInputSerializer,
    responses={
        status.HTTP_200_OK: LoginResponseSerializer,
        status.HTTP_401_UNAUTHORIZED: {'description': 'Credenciais inválidas'},
    },
    examples=[
        OpenApiExample(
            'Exemplo de Login',
            value={
                'cpf': '12345678901',
                'password': 'SenhaSegura@123',
            },
            request_only=True,
        ),
    ],
)
class LoginView(TokenObtainPairView):
    """
    View de login via CPF.
    
    Utiliza o LoginSerializer customizado que retorna dados
    completos do usuário além dos tokens JWT.
    """
    serializer_class = LoginSerializer


@extend_schema(
    tags=['Auth'],
    summary='Atualizar Token de Acesso',
    description='''
    Utiliza o token de refresh para obter um novo token de acesso.
    
    O token de refresh tem validade de 7 dias.
    O novo token de acesso terá validade de 30 minutos.
    ''',
)
class AtualizarTokenView(TokenRefreshView):
    """View para refresh do token de acesso."""
    pass


@extend_schema(
    tags=['Auth'],
    summary='Verificar Token',
    description='Verifica se um token JWT é válido.',
)
class VerificarTokenView(TokenVerifyView):
    """View para verificação de token."""
    pass