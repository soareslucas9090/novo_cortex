from django.utils import timezone

from AppCore.core.helpers.helpers import ModelInstanceHelpers


class UsuarioHelper(ModelInstanceHelpers):
    pass

class CodigoRedefinicaoSenhaHelper(ModelInstanceHelpers):
    
    def esta_valido(self):
        return self.tempo_expiracao > timezone.now()
