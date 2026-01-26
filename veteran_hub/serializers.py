from rest_framework import serializers
from .models import Announcement, UserStats
from users.serializers import UserSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Announcement
        fields = ['id', 'title', 'content', 'priority', 'is_active', 'created_by', 'created_at', 'expires_at']
        read_only_fields = ['created_by']

    def create(self, validated_data):
        validated_data['created_by'] = self.context['request'].user
        return super().create(validated_data)

class UserStatsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserStats
        fields = ['id', 'user', 'posts_count', 'events_joined', 'connections_made', 'resources_shared', 'last_updated']

class DashboardSerializer(serializers.Serializer):
    recent_posts = serializers.ListField(read_only=True)
    upcoming_events = serializers.ListField(read_only=True)
    unread_notifications = serializers.IntegerField(read_only=True)
    user_stats = serializers.DictField(read_only=True)
    announcements = AnnouncementSerializer(many=True, read_only=True)
