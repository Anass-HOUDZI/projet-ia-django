from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('', views.chat_view, name='chat'),
    path('api/send_message/', views.send_message, name='send_message'),
    path('conversation/<int:conversation_id>/export/pdf/', views.export_conversation_pdf, name='export_pdf'),
]
