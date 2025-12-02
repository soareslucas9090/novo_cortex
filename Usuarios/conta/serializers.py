import re

from rest_framework import serializers

from AppCore.common.util.util import validar_senha
from AppCore.core.exceptions.exceptions import ValidationException

from Usuarios.usuario.serializers import UsuarioReferenciaSerializer


# ============================================================================
# SERIALIZERS DE VISUALIZAÇÃO - CÓDIGO DE EMAIL
# ============================================================================

class CodigoEmailContaSerializer(serializers.Serializer):
    """
    Serializer para visualização de código de verificação de email.
    
    Usado para exibir informações sobre o código de verificação.
    Não expõe o código em si por segurança.
    """
    id = serializers.IntegerField(read_only=True)
    email = serializers.EmailField(read_only=True)
    esta_validado = serializers.BooleanField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        """Retorna o status do código de verificação."""
        if obj.esta_validado:
            return 'Validado'
        return 'Pendente'


# ============================================================================
# SERIALIZERS DE VISUALIZAÇÃO - CÓDIGO DE REDEFINIÇÃO DE SENHA
# ============================================================================

class CodigoRedefinicaoSenhaSerializer(serializers.Serializer):
    """
    Serializer para visualização de código de redefinição de senha.
    
    Usado para exibir informações sobre o código (sem expor o código).
    Ideal para admin visualizar códigos pendentes.
    """
    id = serializers.IntegerField(read_only=True)
    usuario = UsuarioReferenciaSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    tempo_expiracao = serializers.DateTimeField(read_only=True)
    validado = serializers.BooleanField(read_only=True)
    status = serializers.SerializerMethodField()
    expirado = serializers.SerializerMethodField()

    def get_status(self, obj):
        """Retorna o status do código de redefinição."""
        from django.utils import timezone
        
        if obj.validado:
            return 'Validado'
        if obj.tempo_expiracao < timezone.now():
            return 'Expirado'
        return 'Pendente'

    def get_expirado(self, obj):
        """Verifica se o código está expirado."""
        from django.utils import timezone
        return obj.tempo_expiracao < timezone.now()


class CodigoRedefinicaoSenhaListaSerializer(serializers.Serializer):
    """
    Serializer resumido para listagem de códigos de redefinição.
    """
    id = serializers.IntegerField(read_only=True)
    usuario = UsuarioReferenciaSerializer(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    validado = serializers.BooleanField(read_only=True)
    expirado = serializers.SerializerMethodField()

    def get_expirado(self, obj):
        """Verifica se o código está expirado."""
        from django.utils import timezone
        return obj.tempo_expiracao < timezone.now()


# ============================================================================
# SERIALIZERS DE INPUT - ESQUECEU SENHA
# ============================================================================

class EsqueceuSenhaSolicitarSerializer(serializers.Serializer):
    """Serializer para solicitar código de redefinição de senha."""
    email = serializers.EmailField(write_only=True)


class ValidarCodigoEmailSerializer(serializers.Serializer):
    """Serializer para validar código de verificação enviado por email."""
    email = serializers.EmailField(write_only=True)
    codigo = serializers.CharField(write_only=True)

    def validate_codigo(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                "O código deve possuir 6 caracteres."
            )
        return value


class EsqueceuSenhaConfirmarSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    codigo = serializers.CharField(write_only=True)
    nova_senha = serializers.CharField(write_only=True)
    confirmar_nova_senha = serializers.CharField(write_only=True)

    def validate_codigo(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                "O código deve possuir 6 dígitos."
            )
        return value

    def validate_nova_senha(self, value):
        try:
            return validar_senha(value)
        except ValidationException as e:
            raise serializers.ValidationError(str(e))

    def validate(self, data):
        if data['nova_senha'] != data['confirmar_nova_senha']:
            raise serializers.ValidationError("As senhas não conferem.")

        return data