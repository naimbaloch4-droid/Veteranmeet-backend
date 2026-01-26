from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .admin_serializers import AdminOverviewSerializer
from users.models import User
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.utils import timezone
from .models import Announcement, UserStats
from .serializers import AnnouncementSerializer, UserStatsSerializer, DashboardSerializer
from posts.models import Post
from events.models import Event
from notifications.models import Notification

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class AnnouncementViewSet(viewsets.ModelViewSet):
    serializer_class = AnnouncementSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsSuperUser()]
        return [IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Announcement.objects.all().order_by('-priority', '-created_at')
        return Announcement.objects.filter(
            is_active=True,
            expires_at__gte=timezone.now()
        ).order_by('-priority', '-created_at')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    user = request.user
    
    # Get or create user stats
    stats, created = UserStats.objects.get_or_create(user=user)
    
    # Refresh stats calculation every time the dashboard is viewed
    stats.posts_count = Post.objects.filter(author=user).count()
    stats.events_joined = user.joined_events.count()
    stats.connections_made = user.star_rating # Using star_rating as 'Connections' impact
    stats.followers_count = user.followers.count()
    stats.following_count = user.following.count()
    stats.resources_shared = 0  
    stats.save()
    
    # Get recent posts
    recent_posts = Post.objects.all()[:5]
    from posts.serializers import PostSerializer
    recent_posts_data = PostSerializer(recent_posts, many=True, context={'request': request}).data
    
    # Get upcoming events
    upcoming_events = Event.objects.filter(date_time__gte=timezone.now())[:5]
    from events.serializers import EventSerializer
    upcoming_events_data = EventSerializer(upcoming_events, many=True, context={'request': request}).data
    
    # Get unread notifications count
    unread_count = Notification.objects.filter(recipient=user, is_read=False).count()
    
    # Get active announcements
    announcements = Announcement.objects.filter(
        is_active=True,
        expires_at__gte=timezone.now()
    )[:3]
    
    dashboard_data = {
        'recent_posts': recent_posts_data,
        'upcoming_events': upcoming_events_data,
        'unread_notifications': unread_count,
        'user_stats': UserStatsSerializer(stats).data,
        'announcements': AnnouncementSerializer(announcements, many=True).data
    }
    
    serializer = DashboardSerializer(dashboard_data)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsSuperUser])
def admin_overview(request):
    """
    General statistics for the Admin Dashboard.
    """
    total_users = User.objects.count()
    total_veterans = User.objects.filter(is_veteran=True).count()
    total_non_veterans = total_users - total_veterans
    active_users = User.objects.filter(is_active=True).count()
    
    total_posts = Post.objects.count()
    total_events = Event.objects.count()
    total_announcements = Announcement.objects.count()
    
    # Recent users (last 10)
    recent_users_queryset = User.objects.all().order_by('-date_joined')[:10]
    from users.serializers import UserSerializer
    recent_users = UserSerializer(recent_users_queryset, many=True).data
    
    # Recent activity summary
    recent_activities = {
        'recent_posts_count': Post.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7)).count(),
        'recent_events_count': Event.objects.filter(created_at__gte=timezone.now() - timezone.timedelta(days=7)).count(),
        'new_users_week': User.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=7)).count()
    }
    
    data = {
        'total_users': total_users,
        'total_veterans': total_veterans,
        'total_non_veterans': total_non_veterans,
        'active_users': active_users,
        'total_posts': total_posts,
        'total_events': total_events,
        'total_announcements': total_announcements,
        'recent_users': recent_users,
        'recent_activities': recent_activities
    }
    
    serializer = AdminOverviewSerializer(data)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_stats(request):
    stats, created = UserStats.objects.get_or_create(user=request.user)
    serializer = UserStatsSerializer(stats)
    return Response(serializer.data)