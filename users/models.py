from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_veteran = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    @property
    def star_rating(self):
        from django.db.models import Sum
        total = self.stars_received.aggregate(total=Sum('quantity'))['total']
        return total or 0

    @property
    def veteran_category(self):
        stars = self.star_rating
        if stars >= 100000:
            return 'Eternal Sage'
        elif stars >= 70000:
            return 'Platinum Veteran'
        elif stars >= 65000:
            return 'Sapphire Veteran'
        elif stars >= 60000:
            return 'Diamond Veteran'
        elif stars >= 50000:
            return 'Golden Veteran'
        elif stars >= 40000:
            return 'Ruby Veteran'
        elif stars >= 25000:
            return 'Silver Veteran'
        else:
            return 'Bronze Veteran'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    military_branch = models.CharField(max_length=50, blank=True)
    service_years = models.CharField(max_length=20, blank=True)
    hobbies = models.TextField(blank=True, help_text="Comma-separated hobbies")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('follower', 'following')

class Star(models.Model):
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars_given', null=True, blank=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='stars_received')
    quantity = models.PositiveIntegerField(default=1)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, related_name='awarded_stars', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('giver', 'receiver', 'event')

    def __str__(self):
        if self.event:
            return f"{self.receiver.username} received {self.quantity} stars for {self.event.title}"
        if self.giver:
            return f"{self.giver.username} gave {self.quantity} star(s) to {self.receiver.username}"
        return f"{self.receiver.username} received {self.quantity} star(s)"

# Signal to update UserStats when stars change
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver as signal_receiver

@signal_receiver(post_save, sender=Star)
@signal_receiver(post_delete, sender=Star)
def update_user_stats(sender, instance, **kwargs):
    try:
        from veteran_hub.models import UserStats
        user = instance.receiver
        if not user:
            return
            
        stats, created = UserStats.objects.get_or_create(user=user)
        # Force a fresh count of the stars from the DB
        stats.connections_made = user.star_rating
        stats.save()
        print(f"SIGNAL: Updated stats for {user.email}. Total: {stats.connections_made}")
    except Exception as e:
        print(f"SIGNAL ERROR: Could not update UserStats: {str(e)}")
