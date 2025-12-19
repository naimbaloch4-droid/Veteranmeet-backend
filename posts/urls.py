from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostListCreateView.as_view(), name='post-list'),
    path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/like/', views.like_post, name='like_post'),
    path('<int:post_id>/comments/', views.CommentListCreateView.as_view(), name='comment_list_create'),
    path('comments/<int:pk>/', views.CommentDetailView.as_view(), name='comment_detail'),
]