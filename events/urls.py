from django.urls import path
from . import views
from .event_features import events_by_hobbies, events_by_location, mark_interested, invite_to_event

app_name = 'events'

urlpatterns = [
    path('', views.EventListCreateView.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event_detail'),
    path('<int:event_id>/join/', views.join_event, name='join_event'),
    path('<int:event_id>/participants/', views.event_participants, name='event_participants'),
    path('by-hobbies/', events_by_hobbies, name='events-by-hobbies'),
    path('by-location/', events_by_location, name='events-by-location'),
    path('<int:event_id>/interested/', mark_interested, name='mark-interested'),
    path('<int:event_id>/invite/', invite_to_event, name='invite-to-event'),
]