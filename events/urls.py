from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListCreateView.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:event_id>/join/', views.join_event, name='join_event'),
    path('<int:event_id>/participants/', views.event_participants, name='event_participants'),
]