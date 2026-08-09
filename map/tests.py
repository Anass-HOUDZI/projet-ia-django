from django.test import Client, TestCase
from django.urls import reverse

from map.models import AdministrativePOI


class MapApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        AdministrativePOI.objects.all().delete()

    def test_api_pois_returns_json(self):
        url = reverse('map:api_pois')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')

        json_data = response.json()
        self.assertEqual(json_data['status'], 'success')
        self.assertIn('pois', json_data)
        self.assertGreaterEqual(len(json_data['pois']), 26)

        poi = json_data['pois'][0]
        self.assertEqual(
            set(poi),
            {
                'id', 'name', 'poi_type', 'address', 'city', 'postal_code',
                'latitude', 'longitude', 'services_offered', 'wait_time_minutes',
            },
        )
        self.assertTrue(any(poi['city'] == 'Paris' for poi in json_data['pois']))
