from django.contrib import admin
from .models import TravelPackage, Booking, DocumentReminder

@admin.register(TravelPackage)
class TravelPackageAdmin(admin.ModelAdmin):
    list_display = ('package_name', 'destination', 'duration', 'price', 'tier', 'is_featured')
    list_filter = ('tier', 'is_featured', 'destination')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'package', 'destination', 'travel_date', 'total_amount', 'status', 'voucher_code')
    list_filter = ('status', 'travel_date')

@admin.register(DocumentReminder)
class DocumentReminderAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'user', 'document_number', 'expiry_date', 'is_verified')
