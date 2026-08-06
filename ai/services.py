import openai
from django.conf import settings
from .models import Message

class ChatbotService:
    def __init__(self):
        # Configuration de l'API Mistral via le client OpenAI
        self.client = openai.OpenAI(
            base_url="https://api.mistral.ai/v1",
            api_key=settings.MISTRAL_API_KEY,
        )
        # Modèle par défaut (Mistral)
        self.model = "mistral-large-latest"
        
        self.system_prompt = (
            "Tu es l'Assistant IA officiel de 'France Étrangers'. "
            "Ton rôle est d'aider les étrangers en France avec leurs démarches administratives. "
            "Règles strictes :\n"
            "1. Va droit au but, fais des phrases courtes.\n"
            "2. N'invente JAMAIS d'informations légales ou de dates. Si tu ne sais pas, dis-le.\n"
            "3. Utilise des listes à puces pour les démarches.\n"
            "4. Demande des précisions sur le profil de l'utilisateur (ex: étudiant, VPF, marié) si tu en as besoin pour affiner ta réponse."
        )

    def generate_response(self, conversation):
        """
        Génère une réponse à partir de l'historique de la conversation.
        """
        # Récupérer l'historique des messages
        db_messages = conversation.messages.order_by('timestamp')
        
        # Préparer les messages pour l'API
        api_messages = [{"role": "system", "content": self.system_prompt}]
        for msg in db_messages:
            # Mistral et OpenAI n'acceptent pas le rôle "ai", il faut utiliser "assistant"
            if msg.role == 'ai':
                api_messages.append({"role": "assistant", "content": msg.content})
            elif msg.role == 'user':
                api_messages.append({"role": "user", "content": msg.content})
            # On ignore les messages techniques 'system' sauvegardés en base pour ne pas polluer l'IA

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=0.3, # Faible créativité pour des réponses factuelles
            )
            ai_content = response.choices[0].message.content
            
            # Sauvegarder la réponse en base
            Message.objects.create(
                conversation=conversation,
                role='ai',
                content=ai_content
            )
            return ai_content
            
        except Exception as e:
            # Fallback en cas d'erreur API
            error_msg = f"Erreur de connexion à l'IA : {str(e)}"
            print(error_msg)
            Message.objects.create(
                conversation=conversation,
                role='system',
                content=error_msg
            )
            return f"Désolé, je rencontre un problème technique. Voici l'erreur exacte pour le développeur : {str(e)}"
