from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from users.models import User
from users.serializers import UserSerializer
from users.views import get_online_users
from .models import ChatRoom, ChatMessage
from .serializers import ChatRoomSerializer, ChatMessageSerializer

class ChatRoomViewSet(viewsets.ModelViewSet):
    serializer_class = ChatRoomSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ChatRoom.objects.none()
        if self.request.user.is_superuser:
            return ChatRoom.objects.all()
        return ChatRoom.objects.filter(participants=self.request.user).distinct()

    @action(detail=True, methods=['get'])
    def sync(self, request, pk=None):
        room = self.get_object()
        last_sync = request.query_params.get('last_sync')
        
        queryset = room.messages.all()
        if last_sync:
            queryset = queryset.filter(created_at__gt=last_sync)
        
        serializer = ChatMessageSerializer(queryset, many=True)
        return Response({
            'messages': serializer.data,
            'server_time': timezone.now().isoformat()
        })

    @action(detail=False, methods=['post'])
    def create_direct_chat(self, request):

        other_user_id = request.data.get('user_id')
        if not other_user_id:
            return Response({'error': 'user_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if direct chat already exists
        existing_room = ChatRoom.objects.filter(
            room_type='direct',
            participants=request.user
        ).filter(participants=other_user_id).first()
        
        if existing_room:
            serializer = self.get_serializer(existing_room)
            return Response(serializer.data)
        
        # Create new direct chat
        room = ChatRoom.objects.create(room_type='direct')
        room.participants.set([request.user.id, other_user_id])
        serializer = self.get_serializer(room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ChatMessage.objects.none()
        room_id = self.request.query_params.get('room_id')
        if room_id:
            queryset = ChatMessage.objects.filter(room_id=room_id)
            if not self.request.user.is_superuser:
                queryset = queryset.filter(room__participants=self.request.user)
            return queryset
        return ChatMessage.objects.none()

    def perform_create(self, serializer):
        message = serializer.save()
        
        # Logic to notify other participants in the room
        room = message.room
        sender = message.sender
        participants = room.participants.exclude(id=sender.id)
        
        from notifications.models import Notification
        for participant in participants:
            Notification.objects.create(
                recipient=participant,
                sender=sender,
                notification_type='message',
                title=f"New message from {sender.username}",
                message=message.content[:100],
                object_id=message.id
            )

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        try:
            # Direct lookup by PK to ensure it exists
            message = ChatMessage.objects.get(pk=pk)
            
            # Security check: User must be in the room
            if not request.user.is_superuser and not message.room.participants.filter(id=request.user.id).exists():
                return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
                
            message.is_read = True
            message.save()
            return Response({'status': 'marked as read'})
        except ChatMessage.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)