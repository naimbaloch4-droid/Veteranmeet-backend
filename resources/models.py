from django.db import models
from users.models import User

class ResourceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Resource Categories"

    def __str__(self):
        return self.name

class Resource(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    url = models.URLField(blank=True)
    contact_info = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(ResourceCategory, on_delete=models.CASCADE, related_name='resources')
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submitted_resources')
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings:
            return sum(r.rating for r in ratings) / len(ratings)
        return 0

class ResourceRating(models.Model):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resource_ratings')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('resource', 'user')

class ResourceBookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookmarked_resources')
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookmarks')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'resource')