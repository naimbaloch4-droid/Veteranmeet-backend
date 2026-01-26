from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SupportGroupViewSet, GroupPostViewSet

router = DefaultRouter()
router.register(r'groups', SupportGroupViewSet, basename='supportgroup')
router.register(r'posts', GroupPostViewSet, basename='grouppost')

urlpatterns = [
    path('', include(router.urls)),
]