from AppCore.core.business.business import ModelInstanceBusiness


class UsuarioBusiness(ModelInstanceBusiness):
    
    def criar_perfil_gestor(self, bio='', avatar=''):
        """
        Cria um perfil de gestor para o usuário.
        
        Args:
            bio: Biografia do perfil
            avatar: Avatar do perfil
            
        Returns:
            Perfil: O perfil criado ou None se já existir
        """
        return self.object_instance.helper.adicionar_perfil(
            tipo_perfil='manager',
            bio=bio,
            avatar=avatar
        )
    
    def obter_perfis_ativos(self):
        """Retorna apenas os perfis ativos do usuário"""
        return self.object_instance.perfis.filter(status=1)
