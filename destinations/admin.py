from django.contrib import admin
from .models import Destination, Review, Hotel, Wishlist, TravelActivity

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'district', 'category', 'average_budget', 'popularity_score', 'rating', 'is_hidden_gem')
    list_filter = ('category', 'district', 'is_hidden_gem', 'eco_friendly')
    search_fields = ('name', 'district', 'description', 'highlights')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('destination', 'user', 'rating', 'sentiment_label', 'sentiment_score', 'created_at')
    list_filter = ('sentiment_label', 'rating')

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price_per_night', 'rating', 'is_eco_friendly')
    list_filter = ('is_eco_friendly', 'destination')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'destination', 'created_at')

@admin.register(TravelActivity)
class TravelActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'activity_type', 'price', 'duration_hours', 'is_eco_friendly')
    list_filter = ('activity_type', 'is_eco_friendly')
