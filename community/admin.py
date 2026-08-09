from django.contrib import admin

from .models import AIModerationLog, Group, Post, Thread

admin.site.register(Group)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(AIModerationLog)
