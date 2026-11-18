from django.contrib import admin
from .models import TravelPreference, UserProfile

@admin.register(TravelPreference)
class TravelPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'preferred_category', 'preferred_climate', 'budget', 'travel_style')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'total_spent', 'budget_limit')
