from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from ai.models import Conversation

def index(request):
    return render(request, 'home.html')

def carnet(request):
    User = get_user_model()
    try:
        user = User.objects.get(username="testuser")
        conversations = Conversation.objects.filter(user=user).order_by('-updated_at')
    except User.DoesNotExist:
        conversations = []
    
    return render(request, 'carnet.html', {'conversations': conversations})

def mentions_legales(request):
    return render(request, 'mentions_legales.html')
