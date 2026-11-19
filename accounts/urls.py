from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('preferences/', views.preferences, name='preferences'),

    # Wishlist, Travel History & Notifications
    path('wishlist/', views.wishlist, name='wishlist'),
    path('wishlist/toggle/<int:dest_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('travel-history/', views.travel_history, name='travel_history'),
    path('notifications/', views.notifications_view, name='notifications'),
]
