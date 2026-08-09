from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock
from ai.models import Conversation, Message
from ai.services import ChatbotService

class ChatbotServiceTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="chat-user", password="test-password")
        self.conversation = Conversation.objects.create(user=self.user, title="Conversation de test")
        Message.objects.create(conversation=self.conversation, role="user", content="Bonjour")

    @patch("ai.services.openai.OpenAI")
    def test_generate_response_success(self, MockOpenAI):
        # Setup mock
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message.content = "Bonjour! Comment puis-je vous aider?"
        mock_client.chat.completions.create.return_value = mock_response

        # Execute
        service = ChatbotService()
        response_text = service.generate_response(self.conversation)

        # Assertions
        self.assertEqual(response_text, "Bonjour! Comment puis-je vous aider?")
        
        # Verify db save
        ai_message = Message.objects.filter(conversation=self.conversation, role="ai").first()
        self.assertIsNotNone(ai_message)
        self.assertEqual(ai_message.content, "Bonjour! Comment puis-je vous aider?")

    @patch("ai.services.openai.OpenAI")
    def test_generate_response_exception(self, MockOpenAI):
        # Setup mock to raise exception
        mock_client = MagicMock()
        MockOpenAI.return_value = mock_client
        mock_client.chat.completions.create.side_effect = Exception("API Error")

        # Execute
        service = ChatbotService()
        response_text = service.generate_response(self.conversation)

        # Assertions
        self.assertTrue(response_text.startswith("Désolé, je rencontre un problème technique."))
        
        # Verify db save
        system_message = Message.objects.filter(conversation=self.conversation, role="system").first()
        self.assertIsNotNone(system_message)
        self.assertIn("API Error", system_message.content)
