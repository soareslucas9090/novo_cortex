from rest_framework import serializers

from Users.users.choices import PERFIL_TIPO_OPCOES
import re


class CriarContaSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    tipo_perfil = serializers.CharField(write_only=True)
    
    def validate_tipo_perfil(self, value):
        tipos_validos = [opcao[0] for opcao in PERFIL_TIPO_OPCOES]

        if value not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de perfil inválido. Escolha entre: {', '.join(tipos_validos)}"
            )

        return value


class ConfirmarCodigoCriarContaSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    codigo = serializers.CharField(write_only=True)
    tipo_perfil = serializers.CharField(write_only=True)

    def validate_codigo(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                "O código deve possuir 6 dígitos."
            )

        return value

    def validate_tipo_perfil(self, value):
        tipos_validos = [opcao[0] for opcao in PERFIL_TIPO_OPCOES]

        if value not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de perfil inválido. Escolha entre: {', '.join(tipos_validos)}"
            )

        return value
    
    
class ConfirmarSenhaCriarContaSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    codigo = serializers.CharField(write_only=True)
    nome = serializers.CharField(max_length=150, write_only=True)
    senha = serializers.CharField(write_only=True)
    confirmar_senha = serializers.CharField(write_only=True)
    telefone = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    data_nascimento = serializers.DateField(required=False, allow_null=True)
    tipo_perfil = serializers.CharField(write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_senha(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
            "A senha deve ter pelo menos 8 caracteres."
            )
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
            "A senha deve conter pelo menos uma letra maiúscula."
            )
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
            "A senha deve conter pelo menos uma letra minúscula."
            )
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
            "A senha deve conter pelo menos um número."
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
            "A senha deve conter pelo menos um caractere especial."
            )
        
        return value
    
    def validate_codigo(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                "O código deve possuir 6 dígitos."
            )
        return value
    
    def validate_tipo_perfil(self, value):
        tipos_validos = [opcao[0] for opcao in PERFIL_TIPO_OPCOES]

        if value not in tipos_validos:
            raise serializers.ValidationError(
                f"Tipo de perfil inválido. Escolha entre: {', '.join(tipos_validos)}"
            )

        return value

    def validate(self, data):
        if data['nova_senha'] != data['confirmar_nova_senha']:    
            raise serializers.ValidationError("As senhas não conferem.")

        return data

class EsqueceuSenhaSolicitarSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    
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
        if len(value) < 8:
            raise serializers.ValidationError(
            "A senha deve ter pelo menos 8 caracteres."
            )
        
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
            "A senha deve conter pelo menos uma letra maiúscula."
            )
        
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError(
            "A senha deve conter pelo menos uma letra minúscula."
            )
        
        if not re.search(r'\d', value):
            raise serializers.ValidationError(
            "A senha deve conter pelo menos um número."
            )
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
            "A senha deve conter pelo menos um caractere especial."
            )
        
        return value

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:    
            raise serializers.ValidationError("As senhas não conferem.")

        return data