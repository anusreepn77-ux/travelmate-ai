from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('destinations/', views.destination_list, name='destination_list'),
    path('destinations/<int:pk>/', views.destination_detail, name='destination_detail'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/add-destination/', views.add_destination, name='add_destination'),
    path('admin-dashboard/create-package/', views.create_package, name='create_package'),
]
