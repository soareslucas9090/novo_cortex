from Usuarios.conta import *

from AppCore.core.exceptions.exceptions import SystemErrorException
from AppCore.core.helpers.helpers import ModelInstanceHelpers

from .models import CodigoEmailConta


class ContaHelper(ModelInstanceHelpers):
    def usuario_com_email_e_tipo_perfil_existe(self, email, tipo_perfil):
        from Usuarios.usuarios.models import Usuario
        
        return Usuario.objects.filter(email=email, perfis__tipo=tipo_perfil).exists()

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
        
    def validar_codigo_valido(self, email, codigo):
        try:
            codigo_email_conta = CodigoEmailConta.objects.get(
            email=email, codigo=codigo, esta_validado=True
            )
            
            codigo_email_conta.delete()
        except Exception as e:
            raise e
