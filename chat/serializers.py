from rest_framework import serializers
from .models import ChatRoom, ChatMessage
from users.serializers import UserSerializer

class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True, required=False)
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = ['id', 'name', 'room_type', 'participants', 'participant_ids', 'last_message', 'created_at', 'updated_at']

    def get_last_message(self, obj):
        last_msg = obj.messages.last()
        if last_msg:
            return ChatMessageSerializer(last_msg).data
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