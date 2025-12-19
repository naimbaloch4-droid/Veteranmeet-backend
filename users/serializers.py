from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User, Profile, Star

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password', 'password_confirm', 'is_veteran')
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        Profile.objects.create(user=user)
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    stars_count = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_veteran', 'profile', 'stars_count')
    
    def get_stars_count(self, obj):
        return obj.stars_received.count()

class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = '__all__'
        read_only_fields = ('giver', 'created_at')