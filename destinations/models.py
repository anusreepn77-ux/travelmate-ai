from django.db import models

class Destination(models.Model):
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    average_budget = models.FloatField()
    best_month = models.CharField(max_length=100, blank=True)
    popularity_score = models.IntegerField(default=50)
    climate = models.CharField(max_length=100, blank=True)
    image = models.ImageField(
        upload_to='destinations/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name