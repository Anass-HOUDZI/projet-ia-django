from django.test import TestCase, Client
from django.urls import reverse

class CommunityViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        url = reverse('community:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'community/index.html')
