from django.utils import timezone

from AppCore.core.helpers.helpers import ModelInstanceHelpers


class UserHelpers(ModelInstanceHelpers):
    
    def add_profile(self, profile_type, bio='', avatar='', status=1):
        from .models import Profile
        
        existing_profile = self.object_instance.profiles.filter(type=profile_type).first()
        if existing_profile:
            return None
        
        profile = Profile.objects.create(
            user=self.object_instance,
            type=profile_type,
            bio=bio,
            avatar=avatar,
            status=status
        )
        return profile
    
    def get_profiles(self):
        """Retorna todos os perfis do usuário"""
        return self.object_instance.profiles.all()
    
    def has_profile_type(self, profile_type):
        """Verifica se o usuário possui um perfil do tipo especificado"""
        return self.object_instance.profiles.filter(type=profile_type).exists()

class PasswordResetCodeHelpers(ModelInstanceHelpers):
    
    def is_valid(self):
        return self.expiration_time > timezone.now()
