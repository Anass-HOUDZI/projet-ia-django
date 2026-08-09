from django.test import Client, TestCase
from django.urls import reverse


class CommunityViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_view(self):
        response = self.client.get(reverse("community:index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "community/index.html")
