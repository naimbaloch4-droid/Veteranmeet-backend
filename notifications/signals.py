from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Like, Comment
from users.models import Star
from events.models import EventParticipant
from .models import Notification

@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.user,
            notification_type='like',
            title='New Like',
            message=f'{instance.user.get_full_name()} liked your post',
            object_id=instance.post.id
        )

@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):
    if created and instance.author != instance.post.author:
        Notification.objects.create(
            recipient=instance.post.author,
            sender=instance.author,
            notification_type='comment',
            title='New Comment',
            message=f'{instance.author.get_full_name()} commented on your post',
            object_id=instance.post.id
        )

@receiver(post_save, sender=Star)
def create_star_notification(sender, instance, created, **kwargs):
    if created:
        sender_name = "System"
        msg = "You received a star"
        
        if instance.giver:
            sender_name = instance.giver.get_full_name() or instance.giver.username
            msg = f'{sender_name} gave you a star'
        elif instance.event:
            msg = f"You earned {instance.quantity} stars for joining: {instance.event.title}"
        
        Notification.objects.create(
            recipient=instance.receiver,
            sender=instance.giver,
            notification_type='star',
            title='New Stars' if instance.quantity > 1 else 'New Star',
            message=msg,
            object_id=instance.id
        )

@receiver(post_save, sender=EventParticipant)
def create_event_join_notification(sender, instance, created, **kwargs):
    if created and instance.user != instance.event.organizer:
        Notification.objects.create(
            recipient=instance.event.organizer,
            sender=instance.user,
            notification_type='event_join',
            title='New Event Participant',
            message=f'{instance.user.get_full_name()} joined your event: {instance.event.title}',
            object_id=instance.event.id
        )