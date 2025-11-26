from Users.account import *

from AppCore.core.exceptions.exceptions import SystemErrorException
from AppCore.core.helpers.helpers import ModelInstanceHelpers

from .models import EmailAccountCode


class AccountHelper(ModelInstanceHelpers):
    def user_with_email_and_type_profile_exists(self, email, type_profile):
        from Users.users.models import User
        
        return User.objects.filter(email=email, profiles__type=type_profile).exists()

    def del_codes_expired(self, email=None):
        if self.object_instance or email:
            if not email:
                email = self.object_instance.email

            EmailAccountCode.objects.filter(
                Q(
                    created_at__lt=timezone.now() - timezone.timedelta(minutes=30)
                ) | Q(
                    email=email
                )
            ).delete()
        
        else:
            raise SystemErrorException('Parâmetros insuficientes para deletar códigos expirados.')
        
    def validate_valid_code(self, email, code):
        try:
            email_account_code = EmailAccountCode.objects.get(
            email=email, code=code, is_validated=True
            )
            
            email_account_code.delete()
        except Exception as e:
            raise e
