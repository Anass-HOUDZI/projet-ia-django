from django.test import TestCase, Client
from django.urls import reverse
from map.models import AdministrativePOI

class MapApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Seed test database with a few POIs
        AdministrativePOI.objects.create(
            name="Test Prefecture",
            poi_type="Préfecture",
            address="123 Test St",
            city="Paris",
            postal_code="75001",
            latitude=48.8566,
            longitude=2.3522,
            services_offered="Test services",
            wait_time_minutes=30
        )

    def test_api_pois_returns_json(self):
        url = reverse('map:api_pois')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        
        json_data = response.json()
        self.assertEqual(json_data['status'], 'success')
        self.assertIn('pois', json_data)
        self.assertTrue(len(json_data['pois']) >= 1)
        
        poi = json_data['pois'][0]
        self.assertEqual(poi['name'], "Test Prefecture")
        self.assertEqual(poi['city'], "Paris")
        self.assertEqual(poi['wait_time_minutes'], 30)
