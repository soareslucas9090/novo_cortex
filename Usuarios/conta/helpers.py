from Usuarios.conta import *

from AppCore.core.exceptions.exceptions import SystemErrorException
from AppCore.core.helpers.helpers import ModelInstanceHelpers

from .models import CodigoEmailConta


class ContaHelper(ModelInstanceHelpers):

    def deletar_codigos_expirados(self, email=None):
        if self.object_instance or email:
            if not email:
                email = self.object_instance.email

            CodigoEmailConta.objects.filter(
                Q(
                    created_at__lt=timezone.now() - timezone.timedelta(minutes=30)
                ) | Q(
                    email=email
                )
            ).delete()
        
        else:
            raise SystemErrorException('Parâmetros insuficientes para deletar códigos expirados.')
