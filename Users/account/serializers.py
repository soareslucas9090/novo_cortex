from rest_framework import serializers

from Users.users.choices import PROFILE_TYPE_CHOICES
import re


class CreateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    type_profile = serializers.CharField(write_only=True)
    
    def validate_type_profile(self, value):
        valid_types = [choice[0] for choice in PROFILE_TYPE_CHOICES]

        if value not in valid_types:
            raise serializers.ValidationError(
                f"Tipo de perfil inválido. Escolha entre: {', '.join(valid_types)}"
            )

        return value


class CreateAccountConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)
    type_profile = serializers.CharField(write_only=True)

    def validate_code(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                "O código deve possuir 6 dígitos."
            )

        return value

    def validate_type_profile(self, value):
        valid_types = [choice[0] for choice in PROFILE_TYPE_CHOICES]

        if value not in valid_types:
            raise serializers.ValidationError(
                f"Tipo de perfil inválido. Escolha entre: {', '.join(valid_types)}"
            )

        return value
    
    
class PasswordConfirmCreateAccountSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)
    name = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    phone = serializers.CharField(max_length=20, required=False, allow_blank=True, allow_null=True)
    birth_date = serializers.DateField(required=False, allow_null=True)
    type_profile = serializers.CharField(write_only=True)
    bio = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    def validate_password(self, value):
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
    
    def validate_code(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                "O código deve possuir 6 dígitos."
            )
        return value
    
    def validate_type_profile(self, value):
        valid_types = [choice[0] for choice in PROFILE_TYPE_CHOICES]

        if value not in valid_types:
            raise serializers.ValidationError(
                f"Tipo de perfil inválido. Escolha entre: {', '.join(valid_types)}"
            )

        return value

    def validate(self, data):
        if data['password'] != data['password_confirm']:    
            raise serializers.ValidationError("As senhas não conferem.")

        return data

class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    
class ForgotPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    code = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    new_password_confirm = serializers.CharField(write_only=True)

    def validate_code(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                "O código deve possuir 6 dígitos."
            )
        return value

    def validate_new_password(self, value):
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