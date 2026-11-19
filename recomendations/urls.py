from django.urls import path
from . import views

urlpatterns = [
    path('', views.assistant_hub, name='assistant_hub'),
    path('ask-ai/', views.ask_ai, name='ask_ai'),
    path('sentiment-api/', views.sentiment_api, name='sentiment_api'),
    path('translate-api/', views.translate_api, name='translate_api'),
    path('connect-buddy/<int:buddy_id>/', views.connect_buddy, name='connect_buddy'),
]
