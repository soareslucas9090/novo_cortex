from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from AppCore.common.texts.messages import (
    USUARIO_INATIVO_OU_SUSPENSO, USUARIO_SEM_PERFIL_CADASTRADO, PERFIL_INATIVO_OU_SUSPENSO
)

from Users.users.choices import USER_STATUS_ATIVO, PROFILE_STATUS_ATIVO, PROFILE_TYPE_CHOICES, PROFILE_TYPE_ADMIN


PROFILE_TYPE_CHOICES_NO_ADMIN = tuple(
    choice for choice in PROFILE_TYPE_CHOICES if choice[0] != PROFILE_TYPE_ADMIN
)

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    type = serializers.ChoiceField(
        choices=PROFILE_TYPE_CHOICES_NO_ADMIN,
        required=False,
        allow_blank=True,
        default='user'
    )
    
    def validate(self, attrs):
        login_type = attrs.pop('type', 'user')
        
        data = super().validate(attrs)
        
        user = self.user
        
        if user.status != USER_STATUS_ATIVO:
            raise serializers.ValidationError({
                'detail': USUARIO_INATIVO_OU_SUSPENSO
            })
        
        profile = user.profiles.filter(type=login_type).first()
        
        if not profile:
            raise serializers.ValidationError({
                'detail': USUARIO_SEM_PERFIL_CADASTRADO % login_type
            })
        
        if profile.status != PROFILE_STATUS_ATIVO:
            raise serializers.ValidationError({
                'detail': PERFIL_INATIVO_OU_SUSPENSO
            })
        
        data['profile'] = {
            'id': profile.id,
            'type': profile.type,
            'type_display': profile.get_type_display()
        }
        
        return data
