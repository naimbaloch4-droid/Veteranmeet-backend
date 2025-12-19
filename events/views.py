from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Event, EventParticipant
from .serializers import EventSerializer, EventParticipantSerializer

class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)

class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def join_event(request, event_id):
    event = get_object_or_404(Event, id=event_id, is_active=True)
    
    if event.participants.count() >= event.max_participants:
        return Response({'error': 'Event is full'}, status=status.HTTP_400_BAD_REQUEST)
    
    participant, created = EventParticipant.objects.get_or_create(
        event=event, 
        user=request.user
    )
    
    if created:
        return Response({'message': 'Successfully joined event'})
    else:
        participant.delete()
        return Response({'message': 'Left event'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def event_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = EventParticipant.objects.filter(event=event)
    serializer = EventParticipantSerializer(participants, many=True)
    return Response(serializer.data)