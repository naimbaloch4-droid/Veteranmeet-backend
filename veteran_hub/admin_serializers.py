from rest_framework import serializers

class AdminOverviewSerializer(serializers.Serializer):
    total_users = serializers.IntegerField()
    total_veterans = serializers.IntegerField()
    total_non_veterans = serializers.IntegerField()
    active_users = serializers.IntegerField()
    total_posts = serializers.IntegerField()
    total_events = serializers.IntegerField()
    total_announcements = serializers.IntegerField()
    recent_users = serializers.ListField()
    recent_activities = serializers.DictField()
