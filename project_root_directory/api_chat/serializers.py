from rest_framework import serializers

from app_core.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ['message', 'response', 'created_at']
        read_only_fields = ['response', 'created_at']
