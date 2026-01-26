from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ResourceCategoryViewSet, ResourceViewSet

router = DefaultRouter()
router.register(r'categories', ResourceCategoryViewSet, basename='resourcecategory')
router.register(r'resources', ResourceViewSet, basename='resource')

urlpatterns = [
    path('', include(router.urls)),
]