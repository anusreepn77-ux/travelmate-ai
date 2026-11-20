from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('destinations/<int:pk>/add-review/', views.add_review, name='add_review'),

    # Admin Dashboard Routes
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/destinations/', views.admin_destinations, name='admin_destinations'),
    path('admin-dashboard/add-destination/', views.add_destination, name='add_destination'),
    path('admin-dashboard/edit-destination/<int:pk>/', views.edit_destination, name='edit_destination'),
    path('admin-dashboard/delete-destination/<int:pk>/', views.delete_destination, name='delete_destination'),

    path('admin-dashboard/create-package/', views.create_package, name='create_package'),
    path('admin-dashboard/edit-package/<int:pk>/', views.edit_package, name='edit_package'),
    path('admin-dashboard/delete-package/<int:pk>/', views.delete_package, name='delete_package'),

    path('admin-dashboard/manage-bookings/', views.manage_bookings, name='manage_bookings'),
    path('admin-dashboard/update-booking/<int:pk>/', views.update_booking_status, name='update_booking_status'),

    path('admin-dashboard/manage-hotels/', views.manage_hotels, name='manage_hotels'),
    path('admin-dashboard/delete-hotel/<int:pk>/', views.delete_hotel, name='delete_hotel'),

    path('admin-dashboard/manage-customers/', views.manage_customers, name='manage_customers'),
    path('admin-dashboard/reports/', views.admin_reports, name='admin_reports'),
]
