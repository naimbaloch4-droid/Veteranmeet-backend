from rest_framework import serializers
from .models import Event, EventParticipant
from users.serializers import UserSerializer

class EventSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    participants_count = serializers.SerializerMethodField()
    is_joined = serializers.SerializerMethodField()
    
    class Meta:
        model = Event
        fields = '__all__'
        read_only_fields = ('organizer', 'created_at', 'updated_at')
    
    def get_participants_count(self, obj):
        return obj.participants.count()
    
    def get_is_joined(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.participants.filter(id=request.user.id).exists()
        return False

class EventParticipantSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = EventParticipant
        fields = '__all__'