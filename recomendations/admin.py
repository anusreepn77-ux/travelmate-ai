from django.contrib import admin
from .models import TravelBuddy, SavedItinerary

@admin.register(TravelBuddy)
class TravelBuddyAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'compatibility_score', 'travel_dates', 'is_active')

@admin.register(SavedItinerary)
class SavedItineraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination_name', 'days', 'estimated_budget', 'created_at')
