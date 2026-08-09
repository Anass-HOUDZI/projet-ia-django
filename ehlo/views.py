from django.contrib.auth import get_user_model
from django.shortcuts import render

from ai.models import Conversation


def index(request):
    return render(request, 'home.html')

def carnet(request):
    user_model = get_user_model()
    try:
        user = user_model.objects.get(username="testuser")
        conversations = Conversation.objects.filter(user=user).order_by('-updated_at')
    except user_model.DoesNotExist:
        conversations = []

    return render(request, 'carnet.html', {'conversations': conversations})

def mentions_legales(request):
    return render(request, 'mentions_legales.html')
