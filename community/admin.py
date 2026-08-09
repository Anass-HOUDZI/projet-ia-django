from django.contrib import admin
from .models import CommunityCategory, CommunityPost, CommunityReply

@admin.register(CommunityCategory)
class CommunityCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'slug')

@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_name', 'category_slug', 'likes_count', 'replies_count', 'sent_to_discord', 'created_at')
    list_filter = ('category_slug', 'sent_to_discord', 'created_at')
    search_fields = ('title', 'content', 'author_name')

@admin.register(CommunityReply)
class CommunityReplyAdmin(admin.ModelAdmin):
    list_display = ('post', 'author_name', 'is_official_answer', 'created_at')
    list_filter = ('is_official_answer', 'created_at')
