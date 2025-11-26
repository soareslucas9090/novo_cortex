import random, string

from AppCore.core.business.business import ModelInstanceBusiness
from AppCore.core.exceptions.exceptions import SystemErrorException
from AppCore.common.util.util import send_simple_email
from AppCore.common.texts.emails import EMAIL_CREATE_ACCOUNT, EMAIL_PASSWORD_RESET_ACCOUNT

from BaseDRFApp import settings
from Users.users.models import User
from .models import EmailAccountCode
from .rules import AccountRule
from .helpers import AccountHelper


class AccountBusiness(ModelInstanceBusiness):
    @property
    def user(self):
        return self.object_instance
    
    def _get_code(self):
        try:
            length_code = 6
            
            return ''.join(random.choices(string.ascii_lowercase, k=length_code))
        except Exception as e:
            raise e

    def get_code(self, email, type_profile):
        try:
            account_rules = AccountRule()

            account_rules.user_profile_dont_exists(email, type_profile)

            account_helper = AccountHelper()
            
            account_helper.del_codes_expired(email)

            random_code = self._get_code()
            
            return EmailAccountCode.objects.create(
                email=email,
                code=random_code
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível gerar o código de verificação.')
        
    def send_verification_email(self, email, email_account_code):
        try:
            send_simple_email(
                "Recuperação de senha",
                f"Código de recuperação de senha: {email_account_code.code}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                EMAIL_CREATE_ACCOUNT % email_account_code.code
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível enviar o email de verificação.')
        
    def validate_code(self, code, email=None):
        if not email:
            email = self.user.email

        try:
            email_account_code = EmailAccountCode.objects.get(
                email=email, code=code
            )

            email_account_code.is_validated = True
            email_account_code.save()
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Código inválido.')
        
    def create_user_account(self, email, code, name, password, phone=None, birth_date=None, type_profile=None, bio=None):
        try:
            account_helper = AccountHelper()
            
            account_helper.validate_valid_code(email, code)
            
            User.objects.create_user(
                email=email,
                name=name,
                password=password,
                phone=phone,
                birth_date=birth_date,
                profiles=[{
                    'type': type_profile,
                    'bio': bio,
                }]
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível criar a conta do usuário.')
    
    def get_code_reset_password(self):
        try:
            self.user.account_helper.del_codes_expired()

            random_code = self._get_code()
            
            return EmailAccountCode.objects.create(
                email=self.user.email,
                code=random_code
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível gerar o código de redefinição de senha.')

    def send_reset_password_email(self, email_account_code):
        try:
            send_simple_email(
                "Redefinição de senha - Código de verificação",
                f"Código de verificação: {email_account_code.code}",
                settings.DEFAULT_FROM_EMAIL,
                [self.user.email],
                EMAIL_PASSWORD_RESET_ACCOUNT % email_account_code.code
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível enviar o email de verificação.')