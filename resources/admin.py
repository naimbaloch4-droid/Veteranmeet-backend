from django.contrib import admin
from .models import ResourceCategory, Resource, ResourceRating, ResourceBookmark

@admin.register(ResourceCategory)
class ResourceCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'location', 'submitted_by', 'is_verified', 'created_at']
    list_filter = ['category', 'is_verified', 'created_at']
    search_fields = ['title', 'description']
    actions = ['mark_verified']

    def mark_verified(self, request, queryset):
        queryset.update(is_verified=True)
    mark_verified.short_description = "Mark selected resources as verified"

@admin.register(ResourceRating)
class ResourceRatingAdmin(admin.ModelAdmin):
    list_display = ['resource', 'user', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']

@admin.register(ResourceBookmark)
class ResourceBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'resource', 'created_at']
    list_filter = ['created_at']