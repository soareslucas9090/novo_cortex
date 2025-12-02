import random, string

from AppCore.core.business.business import ModelInstanceBusiness
from AppCore.core.exceptions.exceptions import NotFoundException, SystemErrorException
from AppCore.common.util.util import enviar_email_simples
from AppCore.common.textos.emails import EMAIL_RESETAR_SENHA_CONTA

from BaseDRFApp import settings
from .models import CodigoEmailConta


class ContaBusiness(ModelInstanceBusiness):
    @property
    def usuario(self):
        return self.object_instance
    
    def _obter_codigo(self):
        try:
            tamanho_codigo = 6
            
            return ''.join(random.choices(string.ascii_lowercase, k=tamanho_codigo))
        except Exception as e:
            raise e
        
    def validar_codigo(self, codigo, email):
        try:
            codigo_email_conta = CodigoEmailConta.objects.get(
                email=email, codigo=codigo
            )

            codigo_email_conta.esta_validado = True
            codigo_email_conta.save()
        except NotFoundException as e:
            raise NotFoundException('Código ou email inválido.')
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível validar o código de redefinição de senha.')
    
    def obter_codigo_redefinicao_senha(self, email):
        try:
            self.usuario.conta_helper.deletar_codigos_expirados(email)

            codigo_aleatorio = self._obter_codigo()
            
            return CodigoEmailConta.objects.create(
                email=email,
                codigo=codigo_aleatorio
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível gerar o código de redefinição de senha.')

    def enviar_email_redefinicao_senha(self, codigo_email_conta, email):
        try:
            enviar_email_simples(
                "Redefinição de senha - Código de verificação",
                f"Código de verificação: {codigo_email_conta.codigo}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                EMAIL_RESETAR_SENHA_CONTA % codigo_email_conta.codigo
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível enviar o email de verificação.')

    def redefinir_senha(self, codigo, email, nova_senha):
        try:
            codigo_email_conta = CodigoEmailConta.objects.get(
                email=email, codigo=codigo, esta_validado=True
            )

            self.usuario.set_password(nova_senha)
            self.usuario.save()

            codigo_email_conta.delete()
        except NotFoundException:
            raise NotFoundException('Código inválido ou não validado.')
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível redefinir a senha.')
