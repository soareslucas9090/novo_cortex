import random, string

from AppCore.core.business.business import ModelInstanceBusiness
from AppCore.core.exceptions.exceptions import SystemErrorException
from AppCore.common.util.util import enviar_email_simples
from AppCore.common.textos.emails import EMAIL_CRIAR_CONTA, EMAIL_RESETAR_SENHA_CONTA

from BaseDRFApp import settings
from Usuarios.usuarios.models import Usuario
from .models import CodigoEmailConta
from .rules import ContaRule
from .helpers import ContaHelper


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

    def obter_codigo(self, email, tipo_perfil):
        try:
            regras_conta = ContaRule()

            regras_conta.perfil_usuario_nao_existe(email, tipo_perfil)

            auxiliar_conta = ContaHelper()
            
            auxiliar_conta.deletar_codigos_expirados(email)

            codigo_aleatorio = self._obter_codigo()
            
            return CodigoEmailConta.objects.create(
                email=email,
                codigo=codigo_aleatorio
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível gerar o código de verificação.')
        
    def enviar_email_verificacao(self, email, codigo_email_conta):
        try:
            enviar_email_simples(
                "Recuperação de senha",
                f"Código de recuperação de senha: {codigo_email_conta.codigo}",
                settings.DEFAULT_FROM_EMAIL,
                [email],
                EMAIL_CRIAR_CONTA % codigo_email_conta.codigo
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível enviar o email de verificação.')
        
    def validar_codigo(self, codigo, email=None):
        if not email:
            email = self.usuario.email

        try:
            codigo_email_conta = CodigoEmailConta.objects.get(
                email=email, codigo=codigo
            )

            codigo_email_conta.esta_validado = True
            codigo_email_conta.save()
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Código inválido.')
        
    def criar_conta_usuario(self, email, codigo, nome, senha, telefone=None, data_nascimento=None, tipo_perfil=None, bio=None):
        try:
            auxiliar_conta = ContaHelper()
            
            auxiliar_conta.validar_codigo_valido(email, codigo)
            
            Usuario.objects.criar_usuario(
                email=email,
                nome=nome,
                senha=senha,
                telefone=telefone,
                data_nascimento=data_nascimento,
                perfis=[{
                    'tipo': tipo_perfil,
                    'bio': bio,
                }]
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível criar a conta do usuário.')
    
    def obter_codigo_redefinicao_senha(self):
        try:
            self.usuario.conta_helper.deletar_codigos_expirados()

            codigo_aleatorio = self._obter_codigo()
            
            return CodigoEmailConta.objects.create(
                email=self.usuario.email,
                codigo=codigo_aleatorio
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível gerar o código de redefinição de senha.')

    def enviar_email_redefinicao_senha(self, codigo_email_conta):
        try:
            enviar_email_simples(
                "Redefinição de senha - Código de verificação",
                f"Código de verificação: {codigo_email_conta.codigo}",
                settings.DEFAULT_FROM_EMAIL,
                [self.usuario.email],
                EMAIL_RESETAR_SENHA_CONTA % codigo_email_conta.codigo
            )
        except self.exceptions_handled as e:
            raise e
        except Exception as e:
            raise SystemErrorException('Não foi possível enviar o email de verificação.')