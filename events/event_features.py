from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Event
from .serializers import EventSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_by_hobbies(request):
    user_hobbies = request.user.profile.hobbies.split(',') if request.user.profile.hobbies else []
    
    events = Event.objects.filter(is_active=True)
    
    # Filter by user's hobbies
    if user_hobbies:
        hobby_filter = Q()
        for hobby in user_hobbies:
            hobby_filter |= Q(hobbies_related__icontains=hobby.strip())
        events = events.filter(hobby_filter)
    
    serializer = EventSerializer(events, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def events_by_location(request):
    city = request.query_params.get('city')
    event_type = request.query_params.get('type')
    
    events = Event.objects.filter(is_active=True)
    
    if city:
        events = events.filter(city__icontains=city)
    if event_type:
        events = events.filter(event_type__icontains=event_type)
    
    serializer = EventSerializer(events, many=True, context={'request': request})
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_interested(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    
    if request.user in event.interested.all():
        event.interested.remove(request.user)
        return Response({'message': 'Removed from interested'})
    else:
        event.interested.add(request.user)
        return Response({'message': 'Marked as interested'})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def invite_to_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    user_ids = request.data.get('user_ids', [])
    
    # Create notifications for invited users
    from notifications.models import Notification
    for user_id in user_ids:
        try:
            from users.models import User
            user = User.objects.get(id=user_id)
            Notification.objects.create(
                user=user,
                message=f"{request.user.username} invited you to {event.title}",
                notification_type='event_invitation'
            )
        except User.DoesNotExist:
            continue
    
    return Response({'message': f'Invitations sent to {len(user_ids)} users'})