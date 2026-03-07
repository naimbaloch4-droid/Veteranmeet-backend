from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import home_view, api_root

urlpatterns = [
    path('', home_view, name='home'),
    path('admin/', admin.site.urls),
    path('api/', api_root, name='api-root'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='schema-swagger-ui'),
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