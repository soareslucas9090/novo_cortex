from rest_framework import serializers


# ============================================================================
# SERIALIZERS DE CARGO
# ============================================================================

class CargoListaSerializer(serializers.Serializer):
    """
    Serializer para listagem de cargos.
    
    Retorna informações básicas do cargo.
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)


class CargoDetalheSerializer(serializers.Serializer):
    """
    Serializer completo para visualização detalhada de um cargo.
    
    Inclui:
    - Dados do cargo
    - Timestamps
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)
    
    # Timestamps
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class CargoResumoSerializer(serializers.Serializer):
    """
    Serializer resumido de cargo para uso em nested serializers.
    """
    id = serializers.IntegerField(read_only=True)
    descricao = serializers.CharField(read_only=True)


# ============================================================================
# SERIALIZERS DE INPUT (Criação/Edição)
# ============================================================================

class CargoCriarSerializer(serializers.Serializer):
    """
    Serializer para criação de um novo cargo.
    
    **Campos obrigatórios:**
    - descricao: Descrição do cargo
    """
    descricao = serializers.CharField(
        max_length=255,
        help_text='Descrição do cargo'
    )

    def validate_descricao(self, value):
        """Valida se já existe um cargo com esta descrição."""
        from EstruturaOrganizacional.cargo.models import Cargo
        if Cargo.objects.filter(descricao=value).exists():
            raise serializers.ValidationError('Já existe um cargo com esta descrição.')
        return value
