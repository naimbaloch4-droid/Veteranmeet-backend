from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Star

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_veteran', 'is_staff')
    list_filter = ('is_veteran', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_veteran',)}),
    )

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'military_branch', 'created_at')
    list_filter = ('military_branch', 'created_at')

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'quantity', 'event', 'created_at')
    list_filter = ('created_at',)
