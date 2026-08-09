from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ai.models import Conversation


class EhloViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.User = get_user_model()
        self.user = self.User.objects.create_user(username='testuser', password='password123')
        self.conversation = Conversation.objects.create(user=self.user, title='Conversation de test')

    def test_index_view(self):
        url = reverse('ehlo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_carnet_view(self):
        url = reverse('carnet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'carnet.html')
        self.assertIn('conversations', response.context)
        self.assertEqual(list(response.context['conversations']), [self.conversation])
