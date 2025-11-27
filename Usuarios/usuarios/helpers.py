from django.utils import timezone

from AppCore.core.helpers.helpers import ModelInstanceHelpers


class UsuarioHelper(ModelInstanceHelpers):
    
    def adicionar_perfil(self, tipo_perfil, bio='', avatar='', status=1):
        from .models import Perfil
        
        perfil_existente = self.object_instance.perfis.filter(tipo=tipo_perfil).first()
        if perfil_existente:
            return None
        
        perfil = Perfil.objects.create(
            usuario=self.object_instance,
            tipo=tipo_perfil,
            bio=bio,
            avatar=avatar,
            status=status
        )
        return perfil
    
    def obter_perfis(self):
        """Retorna todos os perfis do usuário"""
        return self.object_instance.perfis.all()
    
    def tem_tipo_perfil(self, tipo_perfil):
        """Verifica se o usuário possui um perfil do tipo especificado"""
        return self.object_instance.perfis.filter(tipo=tipo_perfil).exists()

class CodigoRedefinicaoSenhaHelper(ModelInstanceHelpers):
    
    def esta_valido(self):
        return self.tempo_expiracao > timezone.now()
