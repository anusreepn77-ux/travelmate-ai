from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from destinations.models import Destination

class TravelPackage(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        related_name='packages'
    )
    package_name = models.CharField(max_length=200)
    duration = models.IntegerField(default=3)
    duration_nights = models.IntegerField(default=2)
    price = models.FloatField()
    description = models.TextField()
    tier = models.CharField(max_length=50, default="Standard")  # Standard, Luxury, Eco
    is_featured = models.BooleanField(default=False)
    image_url = models.URLField(max_length=500, blank=True, default="")

    def __str__(self):
        return f"{self.package_name} (₹{self.price})"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('Confirmed', 'Confirmed'),
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    package = models.ForeignKey(
        TravelPackage,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    travel_date = models.DateField()
    number_of_people = models.IntegerField(default=1)
    total_amount = models.FloatField()
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Confirmed"
    )
    voucher_code = models.CharField(max_length=50, blank=True, default="TM-10492")
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Booking #{self.id} - {self.user.username} ({self.status})"



class DocumentReminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_reminders')
    document_type = models.CharField(max_length=100)  # Passport, ID Card, Kerala Forest Pass, Train/Flight Ticket
    document_number = models.CharField(max_length=100, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.document_type} - {self.user.username}"
