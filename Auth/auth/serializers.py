from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model

from AppCore.common.textos.mensagens import (
    USUARIO_INATIVO_OU_SUSPENSO, USUARIO_SEM_PERFIL_CADASTRADO, PERFIL_INATIVO_OU_SUSPENSO
)

from Usuarios.usuarios.choices import USUARIO_STATUS_ATIVO, PERFIL_STATUS_ATIVO, PERFIL_TIPO_OPCOES, PERFIL_TIPO_ADMIN


PERFIL_TIPO_OPCOES_SEM_ADMIN = tuple(
    opcao for opcao in PERFIL_TIPO_OPCOES if opcao[0] != PERFIL_TIPO_ADMIN
)

Usuario = get_user_model()


class TokenPersonalizadoSerializer(TokenObtainPairSerializer):
    tipo = serializers.ChoiceField(
        choices=PERFIL_TIPO_OPCOES_SEM_ADMIN,
        required=False,
        allow_blank=True,
        default='user'
    )
    
    def validate(self, attrs):
        tipo_login = attrs.pop('tipo', 'user')
        
        data = super().validate(attrs)
        
        usuario = self.user
        
        if usuario.status != USUARIO_STATUS_ATIVO:
            raise serializers.ValidationError({
                'detail': USUARIO_INATIVO_OU_SUSPENSO
            })
        
        perfil = usuario.perfis.filter(tipo=tipo_login).first()
        
        if not perfil:
            raise serializers.ValidationError({
                'detail': USUARIO_SEM_PERFIL_CADASTRADO % tipo_login
            })
        
        if perfil.status != PERFIL_STATUS_ATIVO:
            raise serializers.ValidationError({
                'detail': PERFIL_INATIVO_OU_SUSPENSO
            })
        
        data['perfil'] = {
            'id': perfil.id,
            'tipo': perfil.tipo,
            'exibicao_tipo': perfil.get_tipo_display()
        }
        
        return data
