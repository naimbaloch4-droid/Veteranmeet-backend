from django.contrib import admin
from .models import SupportGroup, GroupMembership, GroupPost

@admin.register(SupportGroup)
class SupportGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic', 'privacy_level', 'admin', 'created_at']
    list_filter = ['privacy_level', 'topic', 'created_at']
    search_fields = ['name', 'description']

@admin.register(GroupMembership)
class GroupMembershipAdmin(admin.ModelAdmin):
    list_display = ['user', 'group', 'role', 'joined_at']
    list_filter = ['role', 'joined_at']

@admin.register(GroupPost)
class GroupPostAdmin(admin.ModelAdmin):
    list_display = ['author', 'group', 'content', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'author__username']