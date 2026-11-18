from django.db import models
from destinations.models import Destination

class TravelPackage(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE
    )

    package_name = models.CharField(max_length=200)
    duration = models.IntegerField()
    price = models.FloatField()
    description = models.TextField()

    def __str__(self):
        return self.package_name


from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    package = models.ForeignKey(
        TravelPackage,
        on_delete=models.CASCADE
    )

    travel_date = models.DateField()
    number_of_people = models.IntegerField(default=1)
    total_amount = models.FloatField()
    status = models.CharField(
        max_length=30,
        default="Pending"
    )