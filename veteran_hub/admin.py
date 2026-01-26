from django.contrib import admin
from .models import Announcement, UserStats

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority', 'is_active', 'created_by', 'created_at', 'expires_at']
    list_filter = ['priority', 'is_active', 'created_at']
    search_fields = ['title', 'content']

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ['user', 'posts_count', 'events_joined', 'connections_made', 'resources_shared', 'last_updated']
    list_filter = ['last_updated']
    search_fields = ['user__username']