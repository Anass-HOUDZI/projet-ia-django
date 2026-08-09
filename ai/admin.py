from django.contrib import admin

from .models import Conversation, DocumentCache, Message

admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(DocumentCache)
