from AppCore.core.business.business import ModelInstanceBusiness


class UserBusiness(ModelInstanceBusiness):
    
    def create_manager_profile(self, bio='', avatar=''):
        """
        Cria um perfil de gestor para o usuário.
        
        Args:
            bio: Biografia do perfil
            avatar: Avatar do perfil
            
        Returns:
            Profile: O perfil criado ou None se já existir
        """
        return self.object_instance.helper.add_profile(
            profile_type='manager',
            bio=bio,
            avatar=avatar
        )
    
    def get_active_profiles(self):
        """Retorna apenas os perfis ativos do usuário"""
        return self.object_instance.profiles.filter(status=1)
