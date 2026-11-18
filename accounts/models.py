from django.db import models
from django.contrib.auth.models import User

class TravelPreference(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='travel_preference'
    )
    interests = models.CharField(max_length=300, default="Nature, Trekking, Scenic Views")
    preferred_climate = models.CharField(max_length=100, default="Cool")
    budget = models.FloatField(default=15000.0)
    preferred_category = models.CharField(max_length=100, default="Hill Station")
    travel_style = models.CharField(max_length=50, default="Solo Explorer")

    def __str__(self):
        return f"Preferences of {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone = models.CharField(max_length=20, blank=True, default="+91 98470 12345")
    bio = models.TextField(blank=True, default="Passionate wanderer exploring the misty peaks and tranquil backwaters of Kerala.")
    avatar_url = models.URLField(max_length=500, blank=True, default="https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=200&q=80")
    total_spent = models.FloatField(default=14200.0)
    budget_limit = models.FloatField(default=25000.0)

    def __str__(self):
        return self.user.username
