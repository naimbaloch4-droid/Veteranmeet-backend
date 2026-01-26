from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import home_view, api_root

schema_view = get_schema_view(
   openapi.Info(
      title="VeteranMeet API",
      default_version='v1',
      description="A comprehensive Django REST API for a veteran community platform with chat, support groups, resources, and hub features",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/auth/', include('users.urls')),
    path('api/events/', include('events.urls')),
    path('api/posts/', include('posts.urls')),
    path('api/notifications/', include('notifications.urls')),
    path('api/chat/', include('chat.urls')),
    path('api/support-groups/', include('support_groups.urls')),
    path('api/resources/', include('resources.urls')),
    path('api/hub/', include('veteran_hub.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)