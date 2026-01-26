from rest_framework import serializers
from .models import ResourceCategory, Resource, ResourceRating, ResourceBookmark
from users.serializers import UserSerializer

class ResourceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ResourceCategory
        fields = ['id', 'name', 'description', 'created_at']

class ResourceSerializer(serializers.ModelSerializer):
    submitted_by = UserSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.ReadOnlyField()
    is_bookmarked = serializers.SerializerMethodField()

    class Meta:
        model = Resource
        fields = ['id', 'title', 'description', 'url', 'contact_info', 'location', 'category', 'category_name', 
                 'submitted_by', 'is_verified', 'average_rating', 'is_bookmarked', 'created_at', 'updated_at']
        read_only_fields = ['submitted_by', 'is_verified']

    def get_is_bookmarked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.bookmarks.filter(user=request.user).exists()
        return False

    def create(self, validated_data):
        validated_data['submitted_by'] = self.context['request'].user
        return super().create(validated_data)

class ResourceRatingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = ResourceRating
        fields = ['id', 'resource', 'user', 'rating', 'review', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class ResourceBookmarkSerializer(serializers.ModelSerializer):
    resource = ResourceSerializer(read_only=True)

    class Meta:
        model = ResourceBookmark
        fields = ['id', 'resource', 'created_at']