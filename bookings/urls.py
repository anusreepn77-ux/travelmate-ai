from django.urls import path
from . import views

urlpatterns = [
    path('book/<int:package_id>/', views.book_package, name='book_package'),
    path('history/', views.booking_history, name='booking_history'),
    path('voucher/<int:booking_id>/', views.voucher_detail, name='voucher_detail'),
]
