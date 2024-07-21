from django.urls import path
from .views import (
    RegistrationAPIView,
    weather_forecast,
    UserDetailView,
    register,
)

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view(), name='registration'),
    path('lk/', UserDetailView.as_view(), name='user_page'),
    path('register/', register, name='register'),
    path('', weather_forecast, name='weather'),
]