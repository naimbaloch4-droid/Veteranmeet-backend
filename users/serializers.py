from rest_framework import serializers
from django.db import models
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

class AdminUserCreateSerializer(UserRegistrationSerializer):
    class Meta(UserRegistrationSerializer.Meta):
        fields = UserRegistrationSerializer.Meta.fields + ('is_superuser', 'is_staff', 'is_active')

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        is_superuser = validated_data.pop('is_superuser', False)
        is_staff = validated_data.pop('is_staff', False)
        
        user = User.objects.create_user(**validated_data)
        user.is_superuser = is_superuser
        user.is_staff = is_staff or is_superuser # Superusers must be staff
        user.save()
        
        Profile.objects.get_or_create(user=user)
        return user

class AdminUserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_veteran', 'is_superuser', 'is_staff', 'date_joined')

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'bio', 'avatar', 'profile_pic', 'location', 'military_branch', 'service_years', 'created_at', 'updated_at', 'user')
        read_only_fields = ('id', 'created_at', 'updated_at', 'user')

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    stars_count = serializers.SerializerMethodField()
    veteran_category = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active', 'is_veteran', 'is_superuser', 'profile', 'stars_count', 'veteran_category', 'date_joined')

    def get_stars_count(self, obj):
        return obj.star_rating

class StarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Star
        fields = '__all__'
        read_only_fields = ('created_at',)
