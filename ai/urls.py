from django.urls import path

from . import views

app_name = 'ai'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/send_message/', views.send_message, name='send_message'),
]
