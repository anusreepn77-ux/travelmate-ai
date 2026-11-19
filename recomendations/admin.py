from django.contrib import admin
from .models import TravelBuddy, SavedItinerary, BuddyConnectionRequest

@admin.register(TravelBuddy)
class TravelBuddyAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'compatibility_score', 'trips_completed', 'is_active')
    list_filter = ('is_active', 'destination')

@admin.register(SavedItinerary)
class SavedItineraryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'destination_name', 'days', 'estimated_budget', 'created_at')

@admin.register(BuddyConnectionRequest)
class BuddyConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_buddy', 'status', 'created_at')
    list_filter = ('status',)
