from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Event, EventParticipant
from .serializers import EventSerializer, EventParticipantSerializer
from users.models import Star

class EventListCreateView(generics.ListCreateAPIView):
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Event.objects.none()
        if self.request.user.is_superuser:
            return Event.objects.all()
        return Event.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Event.objects.none()
        if self.request.user.is_superuser:
            return Event.objects.all()
        return Event.objects.filter(organizer=self.request.user)

    def perform_update(self, serializer):
        # Prevent star_points from being updated after event creation
        if 'star_points' in self.request.data:
            # Remove star_points from update data to prevent changes
            data = self.request.data.copy()
            data.pop('star_points', None)
            serializer.save(**data)
        else:
            serializer.save()

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_event(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id, is_active=True)
        
        participant, created = EventParticipant.objects.get_or_create(
            event=event,
            user=request.user
        )

        if created:
            # Award stars - use get_or_create to avoid duplicates
            star_points = max(event.star_points, 100)
            try:
                star, star_created = Star.objects.get_or_create(
                    receiver=request.user,
                    event=event,
                    defaults={'quantity': star_points}
                )
                
                return Response({
                    'message': 'Successfully joined event',
                    'stars_awarded': star_points,
                    'star_created': star_created,
                    'total_stars': request.user.star_rating
                })
            except Exception as star_error:
                return Response({
                    'message': 'Joined event but star creation failed',
                    'star_error': str(star_error)
                })
        else:
            # Remove stars when leaving
            Star.objects.filter(receiver=request.user, event=event).delete()
            participant.delete()
            return Response({
                'message': 'Left event',
                'total_stars': request.user.star_rating
            })
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = EventParticipant.objects.filter(event=event)
    serializer = EventParticipantSerializer(participants, many=True)
    return Response(serializer.data)