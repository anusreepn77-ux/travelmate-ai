from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:package_id>/', views.book_package, name='book_package'),
    path('history/', views.booking_history, name='booking_history'),
    path('voucher/<int:booking_id>/', views.voucher_detail, name='voucher_detail'),

    # Document Reminders
    path('reminders/add/', views.add_document_reminder, name='add_document_reminder'),
    path('reminders/delete/<int:pk>/', views.delete_document_reminder, name='delete_document_reminder'),

    # Utility Features A & C
    path('multi-destination/', views.multi_destination_explorer, name='multi_destination_explorer'),
    path('nearby-places/', views.nearby_places, name='nearby_places'),
]
