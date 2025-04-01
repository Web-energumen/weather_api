from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APITestCase


class WeatherAPITestCase(APITestCase):
    def test_weather_api_single_date(self):
        url = '/api/v1/weather/Kyiv/2025-05-01/'
        response: Response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('days', response.data)
        self.assertEqual(response.data['days'][0]['datetime'], '2025-05-01')

    def test_weather_api_date_range(self):
        url = '/api/v1/weather/Kyiv/2025-05-01/2025-05-10/'
        response: Response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIn('days', response.data)
        self.assertEqual(len(response.data['days']), 10)
        self.assertEqual(response.data['days'][0]['datetime'], '2025-05-01')
        self.assertEqual(response.data['days'][-1]['datetime'], '2025-05-10')

    def test_weather_api_without_dates(self):
        url = '/api/v1/weather/Kyiv/'
        response: Response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('resolvedAddress', response.data)
        self.assertEqual(response.data['resolvedAddress'], 'Київ, Україна')

        self.assertIn('address', response.data)
        self.assertEqual(response.data['address'], 'Kyiv')

        self.assertIn('days', response.data)
        self.assertEqual(len(response.data['days']), 15)

    def test_weather_api_city_not_found(self):
        url = '/api/v1/weather/NonExistentCity/'
        response: Response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'City not found')
