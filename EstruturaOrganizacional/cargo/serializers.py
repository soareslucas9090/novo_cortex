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


class CargoEditarSerializer(serializers.Serializer):
    """
    Serializer para edição de um cargo existente.
    
    **Campos opcionais:**
    - descricao: Descrição do cargo
    """
    descricao = serializers.CharField(
        max_length=255,
        required=False,
        help_text='Descrição do cargo'
    )

    def validate(self, attrs):
        """Valida se a descrição já existe (exceto para o próprio cargo)."""
        descricao = attrs.get('descricao')
        if descricao:
            from EstruturaOrganizacional.cargo.models import Cargo
            instance = self.context.get('instance')
            queryset = Cargo.objects.filter(descricao=descricao)
            if instance:
                queryset = queryset.exclude(pk=instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({'descricao': 'Já existe um cargo com esta descrição.'})
        return attrs
