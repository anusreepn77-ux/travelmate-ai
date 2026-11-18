from django.urls import path
from . import views

urlpatterns = [
    path('', views.assistant_hub, name='assistant_hub'),
    path('ask-ai/', views.ask_ai, name='ask_ai'),
    path('sentiment-api/', views.sentiment_api, name='sentiment_api'),
]
