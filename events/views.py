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
            # Award stars - ensured minimum 100 stars for joining
            star_points = max(event.star_points, 100)
            
            # Explicitly search with giver=None to match system-awarded stars
            Star.objects.get_or_create(
                receiver=request.user,
                event=event,
                giver=None,
                defaults={'quantity': star_points}
            )
            
            # CRITICAL: Refresh user to pick up new star records
            request.user.refresh_from_db()
            
            print(f"DEBUG: User {request.user.email} joined {event.title}. New Total: {request.user.star_rating}")

            return Response({
                'message': 'Successfully joined event',
                'stars_awarded': star_points,
                'total_stars': request.user.star_rating,
                'category': request.user.veteran_category
            })
        else:
            # Remove stars when leaving
            Star.objects.filter(receiver=request.user, event=event, giver=None).delete()
            participant.delete()
            
            request.user.refresh_from_db()
            
            return Response({
                'message': 'Left event',
                'total_stars': request.user.star_rating,
                'category': request.user.veteran_category
            })
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"CRITICAL ERROR in join_event: {str(e)}\n{error_details}")
        return Response({
            'error': 'Internal Server Error',
            'message': str(e),
            'details': 'Please check server logs for full traceback'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = EventParticipant.objects.filter(event=event)
    serializer = EventParticipantSerializer(participants, many=True)
    return Response(serializer.data)