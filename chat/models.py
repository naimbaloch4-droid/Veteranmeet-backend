from django.db import models
from django.utils import timezone
from datetime import timedelta
from users.models import User

class ChatRoom(models.Model):
    ROOM_TYPE_CHOICES = [
        ('direct', 'Direct'),
        ('group', 'Group'),
    ]
    name = models.CharField(max_length=255, blank=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default='direct')
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    last_message = models.ForeignKey('ChatMessage', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    
    # Typing indicator fields
    typing_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='typing_in_room'
    )
    typing_updated_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['-updated_at']),
        ]

    def __str__(self):
        return self.name or f"Room {self.id}"
    
    def get_typing_user(self):
        """Returns typing user if they typed within last 5 seconds"""
        if self.typing_user and self.typing_updated_at:
            time_diff = timezone.now() - self.typing_updated_at
            if time_diff < timedelta(seconds=5):
                return {
                    'id': self.typing_user.id,
                    'username': self.typing_user.username,
                    'first_name': self.typing_user.first_name,
                    'last_name': self.typing_user.last_name
                }
        return None

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['room', 'created_at']),
            models.Index(fields=['room', 'is_read']),
        ]

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
