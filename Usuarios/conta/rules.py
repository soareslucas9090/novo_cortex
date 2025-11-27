from AppCore.core.rules.rules import ModelInstanceRules

from .helpers import ContaHelper


class ContaRule(ModelInstanceRules):
    def perfil_usuario_nao_existe(self, email, tipo_perfil):
        auxiliar_conta = ContaHelper()
        
        if auxiliar_conta.usuario_com_email_e_tipo_perfil_existe(email, tipo_perfil):
            self.return_exception(
                'Já existe um usuário com este email para este perfil.'
            )
        
        return True
