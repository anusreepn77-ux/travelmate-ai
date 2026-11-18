from django.db import models
from django.contrib.auth.models import User

class TravelPreference(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    interests = models.CharField(max_length=300)
    preferred_climate = models.CharField(max_length=100)
    budget = models.FloatField()
    preferred_category = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username