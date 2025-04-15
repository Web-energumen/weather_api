import time

import requests
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from weather_api.settings import VISUAL_CROSSING_API_KEY


class WeatherAPIView(APIView):
    def get(self, request, location, date1=None, date2=None):
        if not location:
            return Response({'error': 'The location parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        cache_key = f'weather_{location}_{date1}_{date2}'
        cached_data = cache.get(cache_key)

        CACHE_TIMEOUT = 3600 * 6
        if cached_data:
            cached_time = cached_data.get("timestamp")
            if cached_time and time.time() - cached_time < CACHE_TIMEOUT:
                return Response(cached_data["data"])

        api_key = VISUAL_CROSSING_API_KEY
        url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{location}'

        if date1 and date2:
            url += f'/{date1}/{date2}'
        elif date1:
            url += f'/{date1}'

        url += f'?key={api_key}&unitGroup=metric&contentType=json'

        try:
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.json()
                cache.set(cache_key, {"data": weather_data, "timestamp": time.time()}, timeout=CACHE_TIMEOUT)

                return Response(weather_data)

            elif response.status_code == 404:
                return Response({'error': 'City not found'}, status=status.HTTP_404_NOT_FOUND)

            else:
                return Response({'error': 'Failed to retrieve weather data'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except requests.exceptions.RequestException as e:
            return Response({'error': f'Error connecting to the service: {str(e)}'},
                            status=status.HTTP_503_SERVICE_UNAVAILABLE)
