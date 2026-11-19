from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from destinations.models import Destination

class TravelBuddy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buddy_profiles')
    name = models.CharField(max_length=150, default="Explorer")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='buddies')
    travel_dates = models.CharField(max_length=100, default="Oct 24 - Oct 28")
    interests = models.CharField(max_length=250, default="Trekking, Photography, Tea Trails")
    compatibility_score = models.FloatField(default=94.0)
    trips_completed = models.IntegerField(default=6)
    bio = models.TextField(blank=True, default="Solo backpacker who loves early morning peak photography and local food.")
    avatar_url = models.URLField(max_length=500, blank=True, default="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.destination.name} ({self.compatibility_score}%)"


class SavedItinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_itineraries')
    title = models.CharField(max_length=200, default="Kerala Expedition")
    destination_name = models.CharField(max_length=150, default="Munnar")
    days = models.IntegerField(default=3)
    estimated_budget = models.FloatField(default=12000.0)
    itinerary_content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} for {self.user.username}"


class BuddyConnectionRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    )
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_buddy_requests')
    to_buddy = models.ForeignKey(TravelBuddy, on_delete=models.CASCADE, related_name='connection_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, default="Hey! I'd love to travel together.")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('from_user', 'to_buddy')

    def __str__(self):
        return f"{self.from_user.username} → {self.to_buddy.name} ({self.status})"

