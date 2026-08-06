from django.db import models
from django.conf import settings

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Thread(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='threads')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='threads')
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified_by_ai = models.BooleanField(default=False)

    def __str__(self):
        return f"Post by {self.author.username} on {self.thread.title}"

class AIModerationLog(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='moderation_log')
    ai_confidence_score = models.FloatField()
    ai_notes = models.TextField(blank=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for Post {self.post.id}"
