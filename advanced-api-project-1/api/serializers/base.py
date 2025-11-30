from rest_framework import serializers

class BaseSerializer(serializers.Serializer):
    """
    A base serializer that can be extended for various models.
    This can include common fields or methods that are shared across different serializers.
    """
    id = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)