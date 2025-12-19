from django.contrib import admin
from .models import Event, EventParticipant

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'date_time', 'location', 'is_active', 'created_at')
    list_filter = ('is_active', 'date_time', 'created_at')
    search_fields = ('title', 'description', 'location')

@admin.register(EventParticipant)
class EventParticipantAdmin(admin.ModelAdmin):
    list_display = ('event', 'user', 'joined_at')
    list_filter = ('joined_at',)