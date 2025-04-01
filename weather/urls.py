from django.urls import path

from weather.views import WeatherAPIView

app_name = 'weather'

urlpatterns = [
    path('weather/<str:location>/', WeatherAPIView.as_view(), name='get_weather'),
    path('weather/<str:location>/<str:date1>/', WeatherAPIView.as_view(), name='get_weather_single_date'),
    path('weather/<str:location>/<str:date1>/<str:date2>/', WeatherAPIView.as_view(), name='get_weather_range'),
]
