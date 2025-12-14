from rest_framework import serializers
from .models import Notification
from django.contrib.auth import get_user_model

User = get_user_model()

# Notification Serializer
class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField(read_only=True)
    recipient = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Notification
        fields = ['id', 'actor', 'recipient', 'verb', 'target_ct', 'target_id', 'timestamp', 'read']
        read_only_fields = ['actor', 'recipient', 'timestamp']
