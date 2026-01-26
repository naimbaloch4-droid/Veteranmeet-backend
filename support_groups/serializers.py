from rest_framework import serializers
from .models import SupportGroup, GroupMembership, GroupPost
from users.serializers import UserSerializer

class SupportGroupSerializer(serializers.ModelSerializer):
    admin = UserSerializer(read_only=True)
    member_count = serializers.SerializerMethodField()
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = SupportGroup
        fields = ['id', 'name', 'description', 'topic', 'privacy_level', 'admin', 'member_count', 'is_member', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()

    def get_is_member(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.members.filter(id=request.user.id).exists()
        return False

    def create(self, validated_data):
        validated_data['admin'] = self.context['request'].user
        return super().create(validated_data)

class GroupMembershipSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GroupMembership
        fields = ['id', 'user', 'role', 'joined_at']

class GroupPostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = GroupPost
        fields = ['id', 'group', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['author']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)