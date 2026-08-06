from django.contrib import admin
from .models import Group, Thread, Post, AIModerationLog

admin.site.register(Group)
admin.site.register(Thread)
admin.site.register(Post)
admin.site.register(AIModerationLog)
