from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Conversation, Message
from .services import ChatbotService
from django.contrib.auth import get_user_model

def chat_view(request):
    """
    Renders the main chat interface.
    """
    User = get_user_model()
    # Simple hack for testing without login
    user, _ = User.objects.get_or_create(username="testuser", defaults={"nationality": "Inconnue"})
    conversation, _ = Conversation.objects.get_or_create(user=user, title="Mon Assistant IA")
        
    messages = conversation.messages.all().order_by('timestamp')
    return render(request, 'ai/chat.html', {'conversation': conversation, 'messages': messages})

@csrf_exempt
def send_message(request):
    """
    API endpoint to receive a message and return the AI's response.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            conversation_id = data.get('conversation_id')
            content = data.get('content')
            image_base64 = data.get('image_base64')
            
            conversation = Conversation.objects.get(id=conversation_id)
            
            # Save user message
            Message.objects.create(
                conversation=conversation,
                role='user',
                content=content
            )
            
            # Generate AI response
            chatbot = ChatbotService()
            # On passe current_message et image_base64 pour éviter de doubler le message s'il n'y a pas d'image
            # Mais si on l'a déjà sauvegardé en DB, on n'a pas besoin de le repasser si y'a pas d'image
            # S'il y a une image, on passe le dernier message en mode hybride.
            # Pour faire simple, comme db_messages contient déjà le message, on le supprime de api_messages dans generate_response
            # Ah, modifions la façon d'appeler : on ne sauvegarde PAS le message utilisateur AVANT si on a une image ?
            # Non, c'est mieux de le garder en DB (texte seul)
            # En fait j'ai modifié service.py pour prendre current_message, mais s'il est déjà en db, il va être envoyé 2 fois.
            # Changeons le comportement : on passe tout au chatbot.
            ai_response = chatbot.generate_response(conversation, current_message=content if image_base64 else None, image_base64=image_base64)
            
            return JsonResponse({'status': 'success', 'reply': ai_response})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)
