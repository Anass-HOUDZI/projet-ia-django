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
            "Tu es le 'Barista', l'Assistant IA chaleureux et complice du 'Café des Nations'. "
            "Ton rôle est d'aider les étrangers en France avec leurs démarches administratives, tout en gardant un ton rassurant et bienveillant. "
            "Règles strictes :\n"
            "1. Utilise le champ lexical du café avec parcimonie (ex: 'je vous sers cette information', 'installez-vous').\n"
            "2. Va droit au but, fais des phrases courtes et claires.\n"
            "3. N'invente JAMAIS d'informations légales. Si tu ne sais pas, dis-le et renvoie vers service-public.fr.\n"
            "4. Utilise des listes à puces pour les démarches.\n"
            "5. Demande des précisions sur le profil si besoin (étudiant, passeport talent, etc.) de manière conversationnelle."
        )

    def generate_response(self, conversation, current_message=None, image_base64=None):
        """
        Génère une réponse à partir de l'historique de la conversation.
        Accepte un message courant non sauvegardé et une image optionnelle.
        """
        # Récupérer l'historique des messages
        db_messages = conversation.messages.order_by('timestamp')

        # Préparer les messages pour l'API
        api_messages = [{"role": "system", "content": self.system_prompt}]

        # Si current_message est fourni, le dernier message db (qui vient d'être sauvegardé) doit être ignoré dans la boucle
        db_messages_list = list(db_messages)
        if current_message and db_messages_list:
            db_messages_list = db_messages_list[:-1]

        for msg in db_messages_list:
            # Mistral et OpenAI n'acceptent pas le rôle "ai", il faut utiliser "assistant"
            if msg.role == 'ai':
                api_messages.append({"role": "assistant", "content": msg.content})
            elif msg.role == 'user':
                api_messages.append({"role": "user", "content": msg.content})
            # On ignore les messages techniques 'system' sauvegardés en base pour ne pas polluer l'IA

        # Ajouter le message courant s'il y a une image (car il n'est pas encore en base avec l'image)
        if current_message:
            if image_base64:
                # Mode Vision
                self.model = "pixtral-12b-2409"
                vision_content = [
                    {"type": "text", "text": current_message},
                    {"type": "image_url", "image_url": {"url": image_base64}}
                ]
                api_messages.append({"role": "user", "content": vision_content})
                # Surcharge du prompt pour l'analyse de doc
                api_messages[0]["content"] += "\nL'utilisateur a envoyé une image d'un courrier administratif. Extrais: 1. Type de document, 2. Échéances, 3. Actions requises. Format clair. Ajoute un avertissement de toujours vérifier l'original."
            else:
                api_messages.append({"role": "user", "content": current_message})

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
