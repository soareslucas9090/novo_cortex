from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework import status
from rest_framework.permissions import AllowAny

from AppCore.core.exceptions.exceptions import NotFoundException
from AppCore.basics.views.basic_views import BasicPostAPIView
from AppCore.basics.mixins.mixins import AllowAnyMixin
from Users.users.models import User

from .serializers import (
    CreateAccountSerializer, CreateAccountConfirmCodeSerializer,
    PasswordConfirmCreateAccountSerializer, ForgotPasswordRequestSerializer,
    ForgotPasswordConfirmSerializer
)
from .business import AccountBusiness


@extend_schema(tags=["Users.Create account"])
class CreateAccountPostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = CreateAccountSerializer
    success_message = "Código de verificação enviado para o email informado."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        type_profile = serializer.get('type_profile')
        
        account_business = AccountBusiness()

        email_account_code = account_business.get_code(email, type_profile)

        account_business.send_verification_email(email, email_account_code)


@extend_schema(tags=["Users.Create account"])       
class CreateAccountConfirmCodePostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = CreateAccountConfirmCodeSerializer
    success_message = "Código verificado. Você pode prosseguir com a criação da conta."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        code = serializer.get('code')
        
        account_business = AccountBusiness()
        
        account_business.validate_code(email=email, code=code)

        
@extend_schema(tags=["Users.Create account"])
class ConfirmPasswordAccountPostView(BasicPostAPIView, AllowAnyMixin):
    serializer_class = PasswordConfirmCreateAccountSerializer
    success_message = "Usuário criado com sucesso."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        code = serializer.get('code')
        password = serializer.get('password')
        phone = serializer.get('phone')
        birth_date = serializer.get('birth_date')
        type_profile = serializer.get('type_profile')
        bio = serializer.get('bio')
        name = serializer.get('name')
        
        account_business = AccountBusiness()
        account_business.create_user_account(
            email, code, name, password, phone, birth_date, type_profile, bio
        )
        
        return {
            'message': 'Usuário criado com sucesso.',
            'status_code': status.HTTP_201_CREATED
        }


@extend_schema(tags=["Users.Password reset"])
class RequestForgotPasswordCodePostView(AllowAnyMixin, BasicPostAPIView):
    serializer_class = ForgotPasswordRequestSerializer
    success_message = "Código de verificação enviado para o email informado."
    
    def do_action_post(self, serializer, request):
        email = serializer.get('email')
        
        try:
            user = User.objects.get(email=email)
        except NotFoundException:
            raise NotFoundException('Usuário com o email informado não encontrado.')
        
        code_reset = user.account_business.get_code_reset_password()

        user.account_business.send_reset_password_email(code_reset)
