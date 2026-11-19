from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Destination(models.Model):
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    average_budget = models.FloatField(default=5000.0)
    best_month = models.CharField(max_length=100, blank=True, default="October to March")
    popularity_score = models.IntegerField(default=85)
    climate = models.CharField(max_length=100, blank=True, default="Cool & Pleasant")
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    image_url = models.URLField(max_length=500, blank=True, default="")
    
    # Smart Travel & Module 4 Fields
    is_hidden_gem = models.BooleanField(default=False)
    highlights = models.CharField(max_length=300, default="Scenic viewpoints, Cultural heritage, Trekking")
    rating = models.FloatField(default=4.8)
    reviews_count = models.IntegerField(default=1200)
    estimated_days = models.IntegerField(default=3)
    eco_friendly = models.BooleanField(default=True)
    eco_tags = models.CharField(max_length=200, default="Solar Powered, Zero Plastic, Eco-Cottages")
    safety_score = models.IntegerField(default=95)
    crowd_density = models.CharField(max_length=50, default="Moderate")

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        if self.image:
            return self.image.url
        if self.image_url:
            return self.image_url
        return "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80"


class Review(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    review_text = models.TextField()
    sentiment_score = models.FloatField(default=0.85)
    sentiment_label = models.CharField(max_length=30, default="Positive")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.destination.name} - {self.rating}★ by {self.user.username}"


class Hotel(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='hotels')
    name = models.CharField(max_length=200)
    price_per_night = models.FloatField(default=2500.0)
    is_eco_friendly = models.BooleanField(default=True)
    eco_tag = models.CharField(max_length=150, default="Organic Food, Rainwater Harvested")
    rating = models.FloatField(default=4.7)
    image_url = models.URLField(max_length=500, blank=True, default="")

    def __str__(self):
        return f"{self.name} ({self.destination.name})"


class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlists')
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='wishlisted_by')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'destination')

    def __str__(self):
        return f"{self.user.username} ♥ {self.destination.name}"


class TravelActivity(models.Model):
    ACTIVITY_TYPES = (
        ('Sightseeing', 'Sightseeing'),
        ('Adventure', 'Adventure'),
        ('Cultural', 'Cultural'),
        ('Nature', 'Nature'),
        ('Water Sports', 'Water Sports'),
        ('Wellness', 'Wellness'),
    )
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='activities')
    name = models.CharField(max_length=200)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES, default='Sightseeing')
    description = models.TextField(blank=True)
    price = models.FloatField(default=0.0)
    duration_hours = models.FloatField(default=2.0)
    is_eco_friendly = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.destination.name})"
