from django.contrib import admin
from .models import Destination, Review, Hotel

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'category', 'average_budget', 'rating', 'popularity_score', 'is_hidden_gem')
    search_fields = ('name', 'district', 'category', 'highlights')
    list_filter = ('district', 'category', 'is_hidden_gem', 'eco_friendly')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'rating', 'sentiment_label', 'sentiment_score', 'created_at')
    list_filter = ('sentiment_label', 'rating')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price_per_night', 'is_eco_friendly', 'rating')
