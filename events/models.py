from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100, blank=True)
    event_type = models.CharField(max_length=100, blank=True)
    hobbies_related = models.TextField(blank=True, help_text="Comma-separated hobbies")
    date_time = models.DateTimeField()
    max_participants = models.PositiveIntegerField(default=50)
    star_points = models.PositiveIntegerField(default=0, help_text="Stars awarded to participants upon joining")
    organizer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='organized_events')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, through='EventParticipant', related_name='joined_events')
    interested = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interested_events', blank=True)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.star_points > 5000:
            from django.core.exceptions import ValidationError
            raise ValidationError("Event star points cannot exceed 5000")

    class Meta:
        ordering = ['-date_time']

    def __str__(self):
        return self.title

class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
