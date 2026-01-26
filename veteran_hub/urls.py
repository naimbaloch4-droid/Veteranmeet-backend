from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AnnouncementViewSet, dashboard, user_stats, admin_overview

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcement')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard, name='dashboard'),
    path('stats/', user_stats, name='user_stats'),
    path('admin-overview/', admin_overview, name='admin-overview'),
]