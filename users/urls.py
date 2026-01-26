from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views
from .follow_views import follow_user, user_feed

app_name = 'users'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('users/', views.UserViewSet.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('users/<int:pk>/', views.UserViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='user-detail'),
    path('stars/', views.StarListCreateView.as_view(), name='star-list'),
    path('stars/<int:pk>/', views.StarDetailView.as_view(), name='star-detail'),
    path('users/<int:user_id>/stars/', views.UserStarsView.as_view(), name='user-stars'),
    path('give-star/<int:user_id>/', views.give_star, name='give-star'),
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('feed/', user_feed, name='user-feed'),
]
