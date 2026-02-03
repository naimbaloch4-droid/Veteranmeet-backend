from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from users.serializers import UserSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    typing_user = serializers.SerializerMethodField()
    type = serializers.CharField(source='room_type', read_only=True)  # Alias for frontend compatibility

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'type', 'room_type', 'participants', 'participant_ids', 'last_message', 'unread_count', 'typing_user', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        # Use the last_message FK if available for performance
        last_msg = obj.last_message if obj.last_message else obj.messages.last()
        if last_msg:
            return ChatMessageSerializer(last_msg).data
        return None

    def get_unread_count(self, obj):
        """Get unread message count for the current user"""
        request = self.context.get('request')
        if not request or not request.user:
            return 0
        
        # Count messages in this room that are:
        # 1. Not read (is_read=False)
        # 2. Not sent by the current user
        return obj.messages.filter(
            is_read=False
        ).exclude(sender=request.user).count()
    
    def get_typing_user(self, obj):
        """Return typing user if they're currently typing"""
        request = self.context.get('request')
        if not request or not request.user:
            return None
        
        typing_data = obj.get_typing_user()
        if typing_data:
            # Don't show if the typing user is the current user
            if typing_data['id'] != request.user.id:
                return typing_data
        return None

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        room = ChatRoom.objects.create(**validated_data)
        if participant_ids:
            room.participants.set(participant_ids)
        return room

class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'room', 'sender', 'content', 'created_at', 'is_read']
        read_only_fields = ['sender']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)